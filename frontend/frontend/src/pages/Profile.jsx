import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import useAPI from "../hooks/useApi";

import "./Profile.styles.css";

function Profile({ profile }) {
  const { vendorId } = useParams();

  const { data } = useAPI(`/vendor/${vendorId}`);

  useEffect(() => {
    console.log("data:", data);
  }, [data]);

  const navigate = useNavigate();

  const handleOnClick = (serviceId) => {
    navigate(`/service/${serviceId}`);
  };

  console.log(profile);
  if (data) {
    return (
      <div className="vendor-profile">
        <h1>{data.name}</h1>
        <div></div>
        <h2>Services</h2>
        <div className="vendor-services">
          {data.services &&
            data.services.map((s, i) => {
              return (
                <div
                  key={`${s.id}-${i}`}
                  className="vendor-service"
                  onClick={() => handleOnClick(s.id)}
                >
                  <h2>{s.name}</h2>
                  <p>{s.description}</p>
                  <p
                    style={{
                      fontSize: "2rem",
                      fontWeight: 600,
                      textAlign: "right",
                    }}
                  >
                    {s.price} {s.priceCurrency}
                  </p>
                </div>
              );
            })}
        </div>
      </div>
    );
  }
}

export default Profile;
