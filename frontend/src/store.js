const store = {
  token: localStorage.getItem("token") || "",
  isLoggedIn: localStorage.getItem("token") !== null,
};

export default store;
