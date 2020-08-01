import axios from "axios";

const BASE_URL = "/api/buyer";

const retData = (res) => res.data;
const retError = (err) => err.response;

axios.defaults.headers.common = { "Content-Type": "multipart/form-data" };

const getAuthToken = (email, password) => {
  let authData = new FormData();
  authData.set("username", email);
  authData.set("password", password);

  return axios
    .post(`${BASE_URL}/token/`, authData)
    .then(retData)
    .catch(retError);
};

const registerBuyer = (name, email, password) => {
  let authData = new FormData();
  authData.set("name", name);
  authData.set("email", email);
  authData.set("password", password);

  return axios
    .post(`${BASE_URL}/register/`, authData)
    .then(retData)
    .catch(retError);
};

const sendResetPasswordLink = (email) => {
  let emailData = new FormData();
  emailData.set("email", email);

  return axios
    .post(`${BASE_URL}/forget/`, emailData)
    .then(retData)
    .catch(retError);
};

const resetPassword = (token, password) => {
  let resetPasswordData = new FormData();
  resetPasswordData.set("token", token);
  resetPasswordData.set("password", password);

  return axios
    .post(`${BASE_URL}/reset/`, resetPasswordData)
    .then(retData)
    .catch(retError);
};

const validateResetToken = (token) => {
  let tokenData = new FormData();
  tokenData.set("token", token);

  return axios
    .post(`${BASE_URL}/validate/`, tokenData)
    .then(retData)
    .catch(retError);
};

export {
  getAuthToken,
  resetPassword,
  registerBuyer,
  validateResetToken,
  sendResetPasswordLink,
};
