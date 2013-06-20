% Unit Testing with JUnit
% Rami Sayar [@ramisayar](http://twitter/ramisayar)
% May 1st, 2013

## JUnit Introduction

The purpose of this tutorial is to introduce you to unit-testing with JUnit. JUnit is a test framework which uses annotations to construct tests and test suites. It is currently in its fourth version and is widely used in industry, practically the standard framework.

## Some Principles of Testing

* Testing serves to ensure compliance with requirements. Failure is not meeting the requirements.
* Testing should be integrated from inception.
* Start with units and move to integration testing.
* The potential test search space is massive, only cover the most likely situations and edge cases.
* Tests are best written by some one who didn't write the code, who isn't biased.

**Parameters for Testability:**

Good software is testable if the input and output can be observed and if they system can be decomposed to individual independent pieces.

## Types of Testing

Unit-testing is when a test is conducted on a unit such as a class, routine, algorithm, package or small program in the context of a much larger system. The unit-test is conducted in isolation from the rest of the system and tends to be written by the developers.

Integration testing is when a test is conducted on a group of units which interoperate. The group can be composed of two units or the entire system. Integration tests are also conducted by developers. 

Regression testing is when you execute test cases previously passed and ensure that a change did affect other parts of the software.

System testing is when you test the entire system to check if it meets functional requirements.

Acceptance testing is performed by the client to ensure the system meets their requirements and is ready to use.

## Test Driven Development

TDD is an important part of agile software development processes and tends to follow these three rules. [Source Wikipedia](http://en.wikipedia.org/wiki/Test-driven_development)

1. Write tests first.
2. First fail the test cases.
3. Keep the unit small.

## What Makes Code Testable?

Writing testable code is one step you can take to improving the quality of your unit-tests and overall making unit-testing easy. The following are a set of guidelines you can follow to make your code easily testable:

1. The constructor does **not** do real work. You should not be doing anything more complex than value assigning or initialization in your constructors. 
2. Do not pass in objects to be used simply to access other objects.
3. Do not use global state or singletons.
4. Keep your classes simple and your methods short.

## Unit-testing with JUnit

When unit-testing, you will typically have methods in a class which perform a specific test (test method) and typically that class will only contain test methods (test class)

Any class can serve as a test class, thus, JUnit will only look for classes which have the `@Test` annotation attached to a method. 

```
@Test
public void testMultiply() {
   assertEquals("TEST CONDITION 50=50", 50, 50);
 } 
```

JUnit assumes that all test methods are independent and can be executed in an arbitrary order.

## JUnit Annotations

Annotations are used to tell JUnit what the responsibility of a method in a test class is.

* `@Test` executes a method as a test case in the test class.
* `@Before` executes a method once before each test in a class. `@After` executes a method once after each test in a class. 
* `@BeforeClass` executes a method once before any test in a class. `@AfterClass` executes a method once after any test in a class.
* `@Ignore` ignores a test.
* `@Test(expected = Exception.class)` fails a test if it does not throw an exception.
* `@Test(timeout=100)` fails a test if it takes longer than 100 milliseconds.

The order of priority would look like this:

```
@BeforeClass - One Time Set Up
@Before - Set Up
@Test - Test
@After - Tear Down
@Before - Set Up
@Test - Test
@After - Tear Down
@AfterClass - One Time Tear Down
```

Test with Exception Example:

```
@Test(expected = ArithmeticException.class)  
public void divideByZero() {  
    int k = 1/0;
    fail();
}  
```

## JUnit Assert Statements

Assert statements are used to assert a test condition is true. They allow you to specify an error message, the expected result and the actual result.

* fail(string): Purposely fails a test with the string without checking a condition.
* assertTrue(message, condition): Checks if the condition is true.
* assertEquals(message, expected, actual): Checks if the expected and actual value are equal.
* assertEquals(message, expected, actual, tolerance): Checks if the expected and actual value are equal within a tolerance value. This is used to compare floating point values.
* assertNull(message, object)	: Checks if an object is null. assertNotNull(message, object) does the opposite.

## JUnit Test Suite

You can combine several test classes into one test suite and execute all the test cases at once. 

```
import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;

@RunWith(Suite.class)
@SuiteClasses({ MyClassTest.class, MySecondClassTest.class })
public class AllTests {

} 
```

## Test Runner

To run a test class using Java instead of an IDE (such as eclipse), you can use a test runner to execute the test class.

```
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class MyTestRunner {
  public static void main(String[] args) {
    Result result = JUnitCore.runClasses(MyClassTest.class);
    for (Failure failure : result.getFailures()) {
      System.out.println(failure.toString());
    }
  }
}
```

## References

* http://www.vogella.com/articles/JUnit/article.html#unittesting
* http://www.mkyong.com/tutorials/junit-tutorials/

## Integration Testing with Mockito Introduction

The purpose of these notes is to introduce you to integration testing with [Mockito](https://code.google.com/p/mockito/). Mocking is a technique for providing a "mock" representation of resources such as dependencies or "stubs". Mock objects will act as stubs and allow us to verify the interactions between different classes. The Mockito library allows us to create mock objects easily without tediously writing out classes with the appropriate interface. It is one of the easier mocking frameworks to use.

## Mocking a Class

Taking a look back at our Bixi case study and design patterns tutorial, at one point we wanted to create a chain of responsibility to relay messages from a manager to an employee. It's difficult to write a unit-test to verify the behaviour of a chain of responsibility pattern without an integration test. 

Let's recall our example from the design patterns tutorial.

```
abstract class Supervisor {
    protected Supervisor next;
    public void setNext(Supervisor next) {
        this.next = next;
    }
    public void inform(String msg) {        
        if (next != null) {
            next.inform(msg);
        }
    }
}
 
class Manager extends Supervisor {
    public void inform(String msg) {
        // Do something!
        super.inform(msg)
    }
}
 
class Executive extends Supervisor {
    public void inform(String msg) {
        // Do something!
        super.inform(msg)
    }
}

class Mayor extends Supervisor {
    public void inform(String msg) {
        // Do something!
        super.inform(msg)
    }
}
// Creating a Chain
Manager manager = new Manager();
Executive exec = new Executive();
Mayor mayor = new Mayor();
manager.setNext(exec);
exec.setNext(mayor);
```

## Mocking the Chain

In this case, we want to ensure that the message received by the mayor is the current one. Off course, in our test we can inherit from supervisor and verify the rest of each method manually. However, as you can imagine, if the `Supervisor` class was more complicated, we would have to tediously implement many methods manually. Instead, we want to mock a `TestSupervisor` easily. We can do this with mockito.

```
import static org.mockito.Mockito.*;

...

@Test
public void testInteraction(){
    // Creating a mock object.
    Supervisor superv = mock(Supervisor.class);

    Manager manager = new Manager();
    Executive exec = new Executive();
    Mayor mayor = new Mayor();
    manager.setNext(exec);
    exec.setNext(mayor);
    mayor.setNext(superv);

    // Defining behaviour
    when(superv.inform(anyString())).thenReturn(true);

    String m = "message";
    manager.inform(m);

    // Verifying behaviour
    verify(superv, times(1)).inform(m);
}
```

As you can see from the above code, we have created a mock object, defined its behaviour and verified its behaviour.

Creating a mock object is fairly straightforward, you can use the mock method or `@Mock`. However, if you use the annotation method, you need to execute `MockitoAnnotations.initMocks(testClass)` in a test runner or before the tests run.

## Verifying Behaviour

Defining behaviour to be able to verify the interactions follows the 'where x runs return y' pattern. You can specify the arguments for x using any of the below *argument matches*:

* any() - matches any object or null
* anyInt(), anyString(), etc. - matches primitives or their wrappers
* eq(int value), eq(String value), etc. - argument matches the given value
* notNull() - not a null argument
* same(T value) - object argument is the same as the given value
* anyCollection(), anyCollectionOf(java.lang.Class<T>) - matches any collection (generic friendly)
* matches(String regexp) - matches a given regular expression

Verifying the behaviour is as simple as calling verify on the object mock how many times a method was called with a specific parameter. In this case, we want to verify that inform was called once with the parameter m. You can verify that a method is `never()` called, `verifyNoMoreInteractions` or `verifyZeroInteractions(mock1,mock2)`. You can also pass anyString() as the parameter to the method called if you don't care what parameter was passed to it.

## Conclusion

Using mock objects to create stubs and conduct integration tests is extremely powerful. You can develop all the unit tests and integration tests using mock objects without ever writing actual code. Its power lies in allowing you to write tests first and conduct test-driven development. Mockito can do a lot more, take a look at the [Mockito API](http://mockito.googlecode.com/svn/tags/latest/javadoc/org/mockito/Mockito.html).

## Reference

* [Mockito API](http://mockito.googlecode.com/svn/tags/latest/javadoc/org/mockito/Mockito.html)
* [Mockito - Integration testing made easier](http://jnb.ociweb.com/jnb/jnbSep2010.html)