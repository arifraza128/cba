const api = {
  get: async (url) => {
    if (url === "/profile") {
      return {
        data: {
          name: "John Doe",
          email: "john.doe@example.com"
        }
      };
    }
    throw new Error("Not Found");
  }
};

export default api;
