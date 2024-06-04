import { useEffect, useState } from "react";
import useApi from "../hooks/useApi";

function Category({ currentCategory, setCurrentCategory }) {
  const [categoriesData, setCategoriesData] = useState(null);
  const [subCategoriesData, setSubCategoriesData] = useState(null);
  const { data } = useApi("/categories");

  useEffect(() => {
    if (currentCategory) {
      data.map((o, index) => {
        if (o.id == currentCategory) setSubCategoriesData(o.subcategories);
      });
    }
    setCategoriesData(data);
  }, [data, currentCategory]);

  const onClickSelectCategory = (categoryId) => setCurrentCategory(categoryId);

  return (
    <>
      <header>
        <div className="categories">
          {categoriesData &&
            categoriesData.map((o, index) => (
              <p key={index}>
                <a
                  href="#"
                  onClick={() => onClickSelectCategory(o.id)}
                  className={currentCategory == o.id ? "active" : null}
                >
                  {o.name}
                </a>
              </p>
            ))}
        </div>
        <div className="subcategories">
          {subCategoriesData &&
            subCategoriesData.map((o, index) => (
              <p key={index}>
                <a
                  href="#"
                  onClick={() => onClickSelectCategory(o.id)}
                  className={currentCategory == o.id ? "active" : null}
                >
                  {o.name}
                </a>
              </p>
            ))}
        </div>
      </header>
    </>
  );
}

export default Category;
