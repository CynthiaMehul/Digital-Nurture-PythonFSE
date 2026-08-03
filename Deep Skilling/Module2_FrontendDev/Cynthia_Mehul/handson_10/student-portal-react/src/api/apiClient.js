import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 5000,
});

apiClient.interceptors.request.use(
  (config) => {
    config.headers.Authorization = "Bearer mock-token-123";

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    const standardError = new Error(
      error.response?.data?.message ||
        error.message ||
        "Something went wrong"
    );

    standardError.statusCode = error.response?.status || 500;

    return Promise.reject(standardError);
  }
);

export default apiClient;