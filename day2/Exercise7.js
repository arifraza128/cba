let role = "admin";
switch (role) {
    case "admin":
        console.log("Full Access");
        break;
    case "manager":
        console.log("Limited Access");
        break;
    case "employee":
        console.log("Read Only Access");
        break;
    default:
        console.log("Invalid Role");
}