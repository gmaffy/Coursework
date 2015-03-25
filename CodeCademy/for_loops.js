// Example of a for loop:

for (var counter = 1; counter < 11; counter++) {
	console.log(counter);
}

//For loops can be inclusive or exclusive of the final item
for (var i = 4; i <= 23; i = i + 1) {
	console.log(i);
}

//For loops can increment by any amount
for (var i = 5; i <= 50; i+=5) {
	console.log(i);
}

//We can use i++ or i-- to quickly add or subtract 1
for (var i = 5; i >= 0; i--) {
	console.log(i);
}

//An array is an ordered collection of variables of any type
var junk = ['hi','bro',1,2];
console.log(junk);

//Arrays are indexed from 0; this will print the fourth element
var junkData = ["Eddie Murphy", 49, "peanuts", 31];
console.log(junkData[3]);

//A for loop can iterate through the elements of an array
var cities = ["Melbourne", "Amman", "Helsinki", "NYC", "Tokyo", "Seoul"];

for (var i = 0; i < cities.length; i++) {
    console.log("I would like to visit " + cities[i]);
}

var names = ['Light', 'L', 'Takeda', 'Misa Misa', 'Near', 'Mello'];

for (var i = 0; i < names.length; i++) {
    console.log("I know someone called " + names[i]);
}

var names = ["Light", "L", "Near"];

for (var i = 0; i < names.length; i++) {
    if (names[i] === "Light") {
        console.log(names[i]+"?! I hate that guy!");
    }
    else {
        console.log(names[i] + "?! I love that guy!");
    }
}