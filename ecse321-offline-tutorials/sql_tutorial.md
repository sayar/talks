% Databases and SQL
% Rami Sayar [@ramisayar](http://twitter/ramisayar)
% May 1st, 2013

## Introduction

The purpose of this tutorial is to introduce you to databases and SQL. A computer database is a collection of data stored on a computer and may be examined using a program. When one refers to a database such as MySQL typically they are referring to a database management system which may house several databases. Data can be stored and built in several different ways each with its own merits and applications. The model that we will use for this tutorial is the relational database model. 

## Relational Databases

In the relational database model, data is split into tables. Think of tables as Excel spreadsheets, each row is an unit of data and the columns are the different attributes of that data. 

Countries Table
<pre>
id	name	    population
1	Canada	    34million
2	USA         310million
</pre>

City Table
<pre>
id	name        country    population
1	Montreal	 Canada	    2million
2	NYC         USA	        8million		
</pre>

The real power of the relational data model is the ability to reduce data redundancy and to relate units of data with each other. In this model, you can relate a unit of data with another using a one-to-one relationship, a one-to-many relationship or a many-to-one relationship or a many-to-many relationship.

For example, we can see from the two tables above that the data between cities and countries are related and that there is repetition in the country and name columns. We can relate a city without a country using a one-to-one relationship. E.g. Each city is in only one country. However, a country can have many cities so perhaps we should model this relationship as a one-to-many relationship. A many-to-many relationship is a relationship where each unit of data is related to many units and vice-versa.

Primary keys are unique identifiers that can be used to refer to units of data. Foreign keys are links to other units of data which are used to relate to other data.

## SQL

SQL stands for Structured Query Language and is used as a common language to access and manipulate data in a RDBMS. SQL can execute queries, retrieve data, insert, update data as well as create or drop databases and tables. SQL is an ANSI standard. 

## SQL Syntax

SQL is written very differently from the programming languages that you may be familiar with and it is not case-sensitive. It typically follows this syntax:

```
[SQL Command] [column|*] [CLAUSES/CONDITIONS] FROM [table];
```

The most common SQL commands:

* `SELECT` - used to retrieve data
* `UPDATE` - used to update data
* `DELETE` - used to delete data
* `INSERT INTO` - used to insert data


## SELECT Statement

The SELECT statement is used to retrieve data from a database, the result is returned to the caller. The syntax looks like this

```
SELECT column_name,column_name
FROM table_name
```

and

```
SELECT * FROM table_name
```

Sometimes you may have duplicate values in a column, by replaced `SELECT` with `SELECT DISTINCT`, this problem can be solved.

## WHERE Clause

The WHERE clause is used to extract records that match a certain set of conditions. Add `WHERE column_name operator value` at the end of the above SQL command.

```
SELECT * FROM Customers
WHERE Country='Mexico';
```

The operators available are =, <> (not equal), >, <. >=, <=, etc...

You can also chain where clauses using the AND and OR operators.

```
SELECT * FROM Customers
WHERE Country='Germany'
AND City='Berlin';
```

## ORDER BY Clause

The ORDER BY clause allows you to order items by a specific column or multiple columns. The options are descending (DESC) and ascending (ASC).

```
SELECT * FROM Customers
ORDER BY Country DESC;
```

## INSERT Statement

To insert units of data into a table, you have to use the INSERT statement which has the following format:

```
INSERT INTO table_name
VALUES (value1,value2,value3,...)
```

OR

```
INSERT INTO table_name (column1,column2,column3,...)
VALUES (value1,value2,value3,...)
```

E.g.

```
INSERT INTO Customers (CustomerID, CustomerName, City, Country)
VALUES ('Cardinal', 'Stavanger', 'Norway')
```

## UPDATE Statement

To update units of data in a table, you have to use the UPDATE statement which has the following format:

```
UPDATE table_name
SET column1=value, column2=value2,...
WHERE some_column=some_value
```

As you can notice, you have to use the WHERE clause to specify which rows to update, otherwise you may inadvertently update all the rows.

## DELETE Statement

The DELETE statement is used to delete rows in a table, and has the following format:

```
DELETE FROM table_name
WHERE some_column=some_value
```

## What is MySQL?

MySQL is an open source relational database management system. It uses a server-client architecture and is widely used in industry. MySQL is cross-platform, to install the database for your operating system, you can find instructions here: http://dev.mysql.com/doc/refman/5.5/en//installing.html

## JDBC

JDBC stands for Java Database Connectivity and is a data access technology for Java. It provides methods for querying and update data in a RDBMS such as MySQL. When using JDBC, you provide information queries and the results are converted into objects in Java so you can use them just any plain object.

## How Does JDBC Work?

Your java application will call JDBC which then loads a particular driver for the DBMS system you want to talk to, the driver then talks to the database. The application can work with several different types of databases at the same time. You can change database engines without changing application code. 

## Loading JDBC Drivers

To load the driver from MySQL, we can use reflection to load the library.

```
Class.forName("com.mysql.jdbc.Driver");
```

When the driver is loaded, it will register itself with the JDBC DriverManager and prepare itself for execution. You can also manually create an instance of a driver and call 

```
DriverManager.registerDriver(driver);
```

## Connecting to the Database

To connect to a database using a driver, we need to identify its location. JDBC identifies databases using a URL. You give the URL to the driver manager who will then attempt to connect to the database using one of the loaded drivers.

```
Connection con = DriverManager.getConnection("jdbc:some_db", user, password);
```

The connection URL for MySQL typically is in this format:

```
jdbc:mysql://host:port/<db_name>
```

## Interaction with the Database

We create a Statement object using the Connection object. A statement can then execute an SQL query which then returns a ResultSet.

First, we have to create the SQL query. Here we are selecting everything from the Customers table where the Country = Mexico.

```
String queryStr = "SELECT * FROM Customers WHERE Country='Mexico'";
```

Second, create the Java object that will hold the SQL statement.

```
Statement stmt = con.createStatement();
```

Third, use the statement to execute the query string and than store the result in a ResultSet object.

```
ResultSet rs = stmt.executeQuery(queryStr);
```

If we want to execute a statement which will cause a modification to the data (e.g. update or delete the data). We use the `stmt.executeUpdate()` method instead.

## Working with ResultSets

ResultSet objects provide us with access to the results of executing a Statement object. You can use only one ResultSet per Statement. The results are retrieved in sequence, like a List. The current position in the list is maintained by the ResultSet and you advance to the next row by calling `next()`.

In the following example, we will query a coffee table and iterate through the results so that we can print them into the console. Take note of the `while (rs.next())` line of code. 

```
public static void viewTable(Connection con, String dbName)
    throws SQLException {

    Statement stmt = null;
    String query =
        "select COF_NAME, SUP_ID, PRICE, " +
        "SALES, TOTAL " +
        "from " + dbName + ".COFFEES";

    try {
        stmt = con.createStatement();
        ResultSet rs = stmt.executeQuery(query);
        while (rs.next()) {
            String coffeeName = rs.getString("COF_NAME");
            int supplierID = rs.getInt("SUP_ID");
            float price = rs.getFloat("PRICE");
            int sales = rs.getInt("SALES");
            int total = rs.getInt("TOTAL");
            System.out.println(coffeeName + "\t" + supplierID +
                               "\t" + price + "\t" + sales +
                               "\t" + total);
        }
    } catch (SQLException e ) {
        JDBCTutorialUtilities.printSQLException(e);
    } finally {
        if (stmt != null) { stmt.close(); }
    }
}
```

Do not forget to call `close()` on the ResultSet, this will allow you to reuse the Statement object you previous created.

For each row in the result, you can access the specific column of that row by using the following methods.

```
Type getType(int columnIndex)
```

OR

```
Type getType(String columnName)
```

## SQL Types

A topic we did not mention earlier is that data stored into SQL has types that may be different from what you are used to, the following is a mapping of the types:

<table>
	<tr>
		<td>SQL type</td>
		<td>Java Type</td>
	</tr>
	<tr>
		<td>CHAR, VARCHAR, LONGVARCHAR</td>
		<td>String</td>
	</tr>
	<tr>
		<td>NUMERIC, DECIMAL</td>
		<td>java.math.BigDecimal</td>
	</tr>
	<tr>
		<td>BIT</td>
		<td>boolean</td>
	</tr>
	<tr>
		<td>TINYINT</td>
		<td>byte</td>
	</tr>
	<tr>
		<td>SMALLINT</td>
		<td>short</td>
	</tr>
	<tr>
		<td>INTEGER</td>
		<td>int</td>
	</tr>
	<tr>
		<td>BIGINT</td>
		<td>long</td>
	</tr>
	<tr>
		<td>REAL</td>
		<td>float</td>
	</tr>
	<tr>
		<td>FLOAT, DOUBLE</td>
		<td>double</td>
	</tr>
	<tr>
		<td>BIGINT</td>
		<td>long</td>
	</tr>	
	<tr>
		<td>BINARY, BIGINTVARBINARY, LONGVARBINARY</td>
		<td>byte[]</td>
	</tr>
	<tr>
		<td>DATE</td>
		<td>java.sql.Date</td>
	</tr>
	<tr>
		<td>TIME</td>
		<td>java.sql.Time</td>
	</tr>
	<tr>
		<td>TIMESTAMP</td>
		<td>java.sql.Timestamp</td>
	</tr>
</table>

## Null Values

In SQL, NULL simply means that the field in a row is empty. This is not the same as having field with "" or zero. You can ask JDBC if the `ResultSet.wasNull(atColumn);`.

### Timeouts

You will want to prevent queries from stalling your program. You can use the setQueryTimeOut(int seconds) method to set a timeout for the driver to stop the query. An SQLException will be thrown if the query times out.

## Prepared Statements

The majority of the time, your program will spend most of its time executing the same queries. To improve the performance of the program, JDBC offers the ability to parse the SQL query and save it in a PreparedStatement so that you may execute it multiple times without parsing anew each time. 

The PreparedStatement object works differently as you do not want to hard code the values of the query as we did with the regular Statement object. The PreparedStatement offers you the ability to use string interpolation in your query and to change the values each time you execute the query without having to re-parse.

```
String queryStr = "SELECT * FROM employee WHERE superssn= ? and salary > ?";
PreparedStatement pstmt = con.prepareStatement(queryStr);
pstmt.setString(1, "333445555");
pstmt.setInt(2, 26000);
ResultSet rs = pstmt.executeQuery();
```

## ResultSet Meta-Data

When selecting all information from the database, you may not know what columns are being returned. You can find out by using the ResultSetMetaData object. 

```
ResultSetMetaData rsmd = rs.getMetaData(); // rs is a ResultSet object.
int numcols = rsmd.getColumnCount();
for (int i = 1 ; i <= numcols; i++) {
    System.out.print(rsmd.getColumnLabel(i)+" ");
}
```

## Handling Errors

Errors will arise with your SQL code and all errors will be wrapped in an SQLException object. This object will actually contain several exceptions. You can examine them by looping through using the `getNextException()` method.

```
try {
    ...
}
catch (SQLException e) {
    while (e != null) {
        System.out.println(e.getSQLState());
        System.out.println(e.getMessage());
        System.out.println(e.getErrorCode());
        e = e.getNextException();
    }
}
```

## Transactions

Transactions are an important concept in database programming. A transaction is a group of statements that must all succeed or fail together. Depending on your program, you may need to update several tables for a specific action, for example; it could be updating a Customer table and an Order table at the same time. If one of the statements fails to execute correctly, we must be able to reverse the actions taken before or else we may be left with a database in an inconsistent state. The terminology used: commit = completing a transaction, rollback = cancelling a transaction.

How do transactions work? The connection to the database has a state called AutoCommit. If this state is set to true, then every statement is automatically committed. If this state is set to false, then every statement is added to a transaction, the transaction is committed by calling Connection.commit() or rolled back by calling Connection.rollback().

## Conclusion

In this tutorial, we have discussed the relationship database model, the structured query language, the Java interface to databases, transactions and more. Databases are a complex topic, if you are interested, you should register for the database systems course at McGill. 

## References

* [An introduction to databases](http://www.ucl.ac.uk/archaeology/cisp/database/manual/node1.html)
* [W3 Schools](http://www.w3schools.com/sql/default.asp)



