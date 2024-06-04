import { useEffect, useState } from "react";

const APPLICATION_URL =
  import.meta.env.APPLICATION_URL || "http://localhost:8001";

export const fetchData = async (route, options = {}, body = null) => {
  let fetch_options = {
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  };
  if (options) {
    fetch_options = { ...fetch_options, ...options };
  }
  if (body) {
    fetch_options["body"] = JSON.stringify(body);
    fetch_options["method"] = "post";
  }
  console.log(route, fetch_options);
  const response = await fetch(`${APPLICATION_URL}${route}`, fetch_options);
  if (!response.ok) {
    console.error("response error:", response);
    throw new Error(`HTTP error! Status: ${response.status} `);
  }
  const data = await response.json();
  return data;
};

function useAPI(route, body = null, enabled = true) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (enabled) {
      fetchData(route, {})
        .then((d) => {
          setData(d);
        })
        .catch((e) => {
          setError(e);
          console.log(`Net error: ${e}`);
        })
        .finally(() => setIsLoading(false));
    }
  }, [route, body, enabled]);

  return { data, isLoading, error };
}

useAPI.defaultValues = {};

export default useAPI;
