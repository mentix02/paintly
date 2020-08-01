import axios from 'axios';

const BASE_URL = '/api/shop';

axios.defaults.headers.common = {'Content-Type': 'multipart/form-data'};

const getPaintings = () => {
  return axios.get(`${BASE_URL}/`).then(
    response => response.data
  ).catch(
    err => err.response.data
  );
};

export {getPaintings};
