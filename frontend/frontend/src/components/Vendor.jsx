import { useNavigate } from "react-router-dom";
import "./Vendor.styles.css";

function Vendor({ vendor }) {
  const navigate = useNavigate();

  const handleOnClick = (vendorId) => {
    navigate(`/profile/${vendorId}`);
  };

  return (
    <div className="vendor">
      <div
        className="vendor-body"
        onClick={() => handleOnClick(vendor.vendorId)}
      >
        <img src={vendor.profileImageUrl ?? "avatar.jpg"} />
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            columnGap: "1rem",
            alignItems: "start",
          }}
        >
          <h4
            style={{
              margin: 0,
            }}
          >
            {vendor.name}
          </h4>
          <div>
            rating: {vendor.rating} <small>{vendor.vendorId}</small>
          </div>
        </div>
      </div>
      <div className="gallery">
        {vendor.gallery &&
          vendor.gallery.map((pic, i) => (
            <a href="#" key={`${vendor.vendorId}-${i}`}>
              <img src={pic.thumbnailUrl} />
            </a>
          ))}
      </div>
    </div>
  );
}

export default Vendor;
