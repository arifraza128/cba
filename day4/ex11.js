function myPush(arr, value) {
    arr[arr.length] = value;
    return arr.length;
}
let arr1 = [1, 2, 3];
myPush(arr1, 4);
console.log(arr1);
function myPop(arr) {
    if (arr.length === 0) return undefined;
    let last = arr[arr.length - 1];
    arr.length = arr.length - 1;
    return last;
}
let arr2 = [10, 20, 30];
console.log(myPop(arr2));
console.log(arr2);
function myMap(arr, callback) {
    let result = [];
    for (let i = 0; i < arr.length; i++) {
        result[result.length] = callback(arr[i]);
    }
    return result;
}
console.log(myMap([1, 2, 3], x => x * 2));
function myForEach(arr, callback) {
    for (let i = 0; i < arr.length; i++) {
        callback(arr[i], i);
    }
}
myForEach([10, 20, 30], value => console.log(value));
function myObjectKeys(obj) {
    let keys = [];
    for (let key in obj) {
        keys[keys.length] = key;
    }
    return keys;
}
console.log(myObjectKeys({
    name: "Arif",
    age: 21,
    city: "Bengaluru"
}));