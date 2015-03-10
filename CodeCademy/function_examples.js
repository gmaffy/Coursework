//CodeCademy introduction to functions in JavaScript

//Functions in JavaScript follow this format
var print_name = function (argument) {
	console.log(argument); //all lines within the reusable block must end in a semicolon
}

print_name("Phil"); //call functions like this

//Can also return values
var timesTwo = function (number) {
	return number * 2;
}

var newNumber = 5;
console.log(timesTwo(newNumber));

//Returned values can be used like any other values in JavaScript
//This simple example shows how a function can be used to check whether a value is divisible by 3 and 4
var quarter = function (number) {
    return number / 4;
}

if (quarter(12) % 3 === 0 ) {
  console.log("The statement is true");
} else {
  console.log("The statement is false");
}

//Functions can take multiple arguments
var perimeterBox = function (length, width) {
    return 2 * (length + width);
}

console.log(perimeterBox(1,2))


//Similar to Python, JavaScript has variable scoping rules
//The keyword var defines a variable within the current scope
//Global variables are still accessible within function namespaces
var my_number = 7; //this has global scope

var timesTwo = function(number) {
    var my_number = number * 2; //this has local scope
    console.log("Inside the function my_number is: ");
    console.log(my_number);
}; 

timesTwo(7);

console.log("Outside the function my_number is: ")
console.log(my_number);

//Functions can return values in a conditional fashion
var sleepCheck = function (numHours) {
    if (numHours >= 8) {
        return "You're getting plenty of sleep! Maybe even too much!";
    }
    else {
        return "Get some more shut eye!";
    }
}

console.log(sleepCheck(10));
console.log(sleepCheck(5));
console.log(sleepCheck(8));