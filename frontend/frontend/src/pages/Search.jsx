import { useEffect, useState } from "react";
import Category from "../components/Category";
import Vendor from "../components/Vendor";
import useAPI from "../hooks/useApi";
import "./Search.styles.css";

function Search() {
  const [currentCategory, setCurrentCategory] = useState(null);

  const [filter, setFilter] = useState({
    categoryId: "380a9add-4f08-44ec-b4cb-9af43bd1311e",
    coord: {
      latitude: 25,
      longitude: 55.1646,
    },
    pagination: {
      offset: 0,
      limit: 100,
    },
    filters: {},
  });

  const { data } = useAPI("/search", filter, filter.categoryId != null);

  useEffect(
    () =>
      setFilter({
        ...filter,
        filters: { ...filter.filters },
        categoryId: currentCategory,
      }),
    [currentCategory]
  );

  useEffect(() => {
    console.log(data);
  }, [data]);

  return (
    <>
      <div className="search">
        <div className="search-panel">
          <header>
            <h2>Search</h2>
            <Category
              currentCategory={currentCategory}
              setCurrentCategory={setCurrentCategory}
            />
          </header>
        </div>
        <div
          className="search-box"
          style={{
            margin: "1rem 0",
            display: "flex",
            flexDirection: "column",
            rowGap: "1rem",
          }}
        >
          <div>
            <input className="search-input" placeholder="search request here" />
          </div>
          {data &&
            data.profiles.map((vendor, i) => (
              <Vendor vendor={vendor} key={`${i}-${vendor.vendorId}`} />
            ))}
        </div>
      </div>
    </>
  );
}

export default Search;
