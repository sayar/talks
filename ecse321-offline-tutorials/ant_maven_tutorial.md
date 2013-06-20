% Ant Tutorial
% Rami Sayar [@ramisayar](http://twitter/ramisayar)
% May 1st

## Introduction to Ant

The purpose of this tutorial is to introduce you to building and compiling things with ant. Ant is a tool often used to build Java applications. Ant supplies built-in tasks to compile, assemble, test and run Java applications using a build file.

## Getting Ant

1. Make sure you have a Java environment installed.
1. Download Ant from [ant.apache.org](http://ant.apache.org/)
1. Uncompress the downloaded file into a directory.
1. Set environmental variables JAVA_HOME to your Java environment, ANT_HOME to the directory you uncompressed Ant to, and add ${ANT_HOME}/bin (Unix) or %ANT_HOME%/bin (Windows) to your PATH.

NOTE: You should verify if you already have ant installed. 

## Project Preparation

Ideally, you want to generate class files to a different location than the same directory as your source files. Typically, you will have a `classes` or `objects` folder for compiled files, `jar` or `bin` for a jar or executable file and a `src` or `source` directory.

To do the above using the compiler directly can become complex and unwieldy for large projects. See below for an example.

1. Create directory for compiler outputs and source code.

```
mkdir -p build/classes build/jar src
```

2. Create a HelloWorld program.

```
vim src/HelloWorld.java
```

3. Compile the java files, make sure to set the appropriate paths.

```
javac -sourcepath src -d build/classes src/HelloWorld.java
```

4. Run the compiled java program.

```
java -cp build/classes HelloWorld
```

## Ant to the Rescue!

If we have more files, more directories, dependencies on other jar files, a more complicated build process, etc… it becomes unnecessarily difficult to interface with the compiler directly, tedious, error prone and genuinely unpleasant.

Perhaps, you need a more complicated build process than the one described above. Perhaps, you need to download the source before compiled, prepare a build area by creating standard set of directories, configure the source code, validate it, compile it, test it, zip the executable, build documentation, etc… 

Build tools allow you to describe your build process, the dependencies between the steps, execute and manage the build, etc… without forcing every developer on a team to know the intimate details of the process. The build tool manages the build process for you and handles all of the details and steps. Ant provides you with a set of tools and techniques to define a build process and execute it. 

## Ant Build Files

Ant uses a build.xml file to describe your process and is typically placed at the root of your project directory. Ant uses xml to describe the build process, the following a simple example to do what we did above using the command line directly with the exception that we also added the ability to generate a build file.

NOTE: The example code is taken from [the official Apache Ant tutorial](http://ant.apache.org/manual/tutorial-HelloWorldWithAnt.html)

```
<project>
    <!-- Clean target which deletes the build directory. -->
    <target name="clean">
        <delete dir="build"/>
    </target>

    <!-- Create the output directory. Compile targets from src into build/classes. -->
    <target name="compile">
        <mkdir dir="build/classes"/>
        <javac srcdir="src" destdir="build/classes"/>
    </target>

    <!-- Create the output directory. Build the jar file from the compiled classes. -->
    <target name="jar">
        <mkdir dir="build/jar"/>
        <jar destfile="build/jar/HelloWorld.jar" basedir="build/classes">
            <manifest>
                <attribute name="Main-Class" value="HelloWorld"/>
            </manifest>
        </jar>
    </target>

    <!-- Run the jar. -->
    <target name="run">
        <java jar="build/jar/HelloWorld.jar" fork="true"/>
    </target>

</project>
```

Looking at the above build.xml file, we see a root node called project and several children called target. Each target has a name attribute which identifies what the target does. Inside each target you will see several nodes. The first node we can see is delete which simply deletes a directory or file. The second node is mkdir which simple creates a directory. The next node of interest is javac, this is very similar to the javac command line interface, we can set a source directory, a destination directory and more. The next node of interest is the jar node, which also has a child called manifest which allows us to set attributes to the jar file, such as a `Main-Class`. The last node of interest is the java node, which allows us to specify a jar to run with a fork (in another process).

To compile, build and run any of the targets above, you can execute the following in the root directory. `ant TARGET_NAME`

```
ant compile
ant jar
ant run
```

```
ant compile jar run
```

## Enhancing the Build File

Let's enhance the above build process to include nomenclature and cleaning mechanism to remove previously build class files. In this example, we set key-value properties as you can see from the property xml tags. We can also refer to properties using the `${name}` syntax. The compile target was updated to reference the properties set earlier in the file. 

```
<project name="HelloWorld" basedir="." default="main">
    <property name="src.dir"     value="src"/>
    <property name="build.dir"   value="build"/>
    <property name="classes.dir" value="${build.dir}/classes"/>
    <property name="jar.dir"     value="${build.dir}/jar"/>
    <property name="main-class"  value="HelloWorld"/>

    <target name="clean">
        <delete dir="${build.dir}"/>
    </target>

    <target name="compile">
        <mkdir dir="${classes.dir}"/>
        <javac srcdir="${src.dir}" destdir="${classes.dir}"/>
    </target>

    <target name="jar" depends="compile">
        <mkdir dir="${jar.dir}"/>
        <jar destfile="${jar.dir}/${ant.project.name}.jar" basedir="${classes.dir}">
            <manifest>
                <attribute name="Main-Class" value="${main-class}"/>
            </manifest>
        </jar>
    </target>

    <target name="run" depends="jar">
        <java jar="${jar.dir}/${ant.project.name}.jar" fork="true"/>
    </target>

    <target name="clean-build" depends="clean,jar"/>

    <target name="main" depends="clean,run"/>

</project>
```

The new nodes such as property allow us to set a key-value which we can then refer to in other places in the build process using the `${}` mechanism. 

## Managing Dependencies

Large java software projects will typically use many libraries and as a result have multiple dependencies. A common library used by java projects is Log4J. To integrate log4j into your project, you would download the latest jar and add it to a `lib` directory in you project root folder, you would then have to make that log4j is in your classpath for your project to compile. Handling dependencies is a perfect use case for build tools. Let's modify our above build.xml to add support for a `lib` directory and automatically adding jars to the class path.

```
<project name="HelloWorld" basedir="." default="main">
    ...
    <property name="lib.dir" value="lib"/>

    <path id="classpath">
        <fileset dir="${lib.dir}" includes="**/*.jar"/>
    </path>
    ...
    <target name="compile">
        <mkdir dir="${classes.dir}"/>
        <javac srcdir="${src.dir}" destdir="${classes.dir}" classpathref="classpath"/>
    </target>

    <target name="run" depends="jar">
        <java fork="true" classname="${main-class}">
            <classpath>
                <path refid="classpath"/>
                <path location="${jar.dir}/${ant.project.name}.jar"/>
            </classpath>
        </java>
    </target>
    ...
</project>
```

Above you can see we specified a path node to easily reference paths in our build process, this is then used to build the classpath list in the run and compile mode. 

## Conclusion to Ant

The above notes should be enough to give you a taste of Ant and to get you started with a simple build process for your project. Ant offers many built-in tools which can simplify your life. I highly recommend you take a look at the Ant documentation to learn more.

## References

* [Tutorial: Hello World with Apache Ant](http://ant.apache.org/manual/tutorial-HelloWorldWithAnt.html)
* [What is Ant?](http://codefeed.com/tutorial/ant_intro.html)

## Introduction to Maven

Maven is another tool similar to Ant. Maven takes a more opinionated approach about how to generate, compile and run your projects. It expects a standard project structure. 

To generate a basic maven project, you can run the following command:

```
mvn archetype:generate -DgroupId=com.mycompany.app -DartifactId=my-app \
    -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

This will generate the following project structure inside a my-app directory.

```
my-app
|-- pom.xml
`-- src
    |-- main
    |   `-- java
    |       `-- com
    |           `-- mycompany
    |               `-- app
    |                   `-- App.java
    `-- test
        `-- java
            `-- com
                `-- mycompany
                    `-- app
                        `-- AppTest.java
```

## Installing Maven

Download maven for your distribution from [here](http://maven.apache.org/download.cgi). The following instructions are for Unix-based systems. You can find instructions for Windows [here](http://maven.apache.org/download.cgi).

1. Extract the distribution archive, i.e. apache-maven-3.0.5-bin.tar.gz to the directory you wish to install Maven 3.0.5. These instructions assume you chose /usr/local/apache-maven. The subdirectory apache-maven-3.0.5 will be created from the archive.
1. In a command terminal, add the M2_HOME environment variable, e.g. export M2_HOME=/usr/local/apache-maven/apache-maven-3.0.5.
1. Add the M2 environment variable, e.g. export M2=$M2_HOME/bin.
1. Add M2 environment variable to your path, e.g. export PATH=$M2:$PATH.
1. Make sure that JAVA_HOME is set to the location of your JDK, e.g. export JAVA_HOME=/usr/java/jdk1.5.0_02 and that $JAVA_HOME/bin is in your PATH environment variable.
1. Run mvn --version to verify that it is correctly installed.


## The Maven POM File

Maven will generate a `pom.xml` which describes the project's configuration, this is similar to the `build.xml` file generated by Ant. 

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.mycompany.app</groupId>
  <artifactId>my-app</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <name>Maven Quick Start Archetype</name>
  <url>http://maven.apache.org</url>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.8.2</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```

As you can see in the above xml, you can change the name of the project, the project url and ()what is extremely interesting about maven) the dependencies tag. In Ant, you had to manually manage the dependencies and add them to a lib folder before being able to compile them into the project. With Maven, you can simply write the identification of the dependencies (groupId, artifactId), the version you want and maven will handle downloading the dependency and including it in the build path.

## Building with Maven

To build with Maven you simply run  `mvn package`. Maven also lets you run different pieces of the lifestyle process without you having to manually define them (as in Ant). 

* validate: validate the project is correct and all necessary information is available
* compile: compile the source code of the project
 test: test the compiled source code using a suitable unit testing framework. These tests should not require the code be packaged or deployed
package: take the compiled code and package it in its distributable format, such as a JAR.
* integration-test: process and deploy the package if necessary into an environment where integration tests can be run
* verify: run any checks to verify the package is valid and meets quality criteria
* install: install the package into the local repository, for use as a dependency in other projects locally
* deploy: done in an integration or release environment, copies the final package to the remote repository for sharing with other developers and projects.
* clean: cleans up artifacts created by prior builds

You can also run the above commands in a specific sequence just like ant.

```
mvn clean dependency:copy-dependencies package
```

## Conclusion

The above note is a small introduction to maven. Maven is a very powerful technology which does things in a specific, standard way.

## References

* [Maven](http://maven.apache.org)
* [Maven in 5 Minutes](http://maven.apache.org/guides/getting-started/maven-in-five-minutes.html)