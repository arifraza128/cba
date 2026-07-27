const user = {
    name: "Rahul",
    age: 25
};
user["email"] = "rahul@gmail.com";
delete user.age;
for (let key in user) {
    console.log(key, user[key]);
}
console.log("email" in user);