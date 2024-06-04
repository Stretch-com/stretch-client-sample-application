import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import useAPI from "../hooks/useApi";

import "./Profile.styles.css";

function Service({ profile }) {
  const { serviceId } = useParams();

  const [slots, setSlots] = useState(null);

  const { data } = useAPI(`/availability/${serviceId}`, null, slots == null);
  const [booking, setBooking] = useState(null);

  useEffect(() => {
    console.log("data:", data);
    setSlots(data);
  }, [data]);

  const navigate = useNavigate();

  const convertDate = (date) => {
    var date = new Date(date);
    return date.toLocaleString(); // "Wed Jun 29 2011 09:52:48 GMT-0700 (PDT)"
  };

  //   const { booking_data } = useAPI("/booking", booking, booking != null);

  const handlerBooking = (serviceId, slots) => {
    const bookingData = {
      customerId: "1",
      username: "TestUser",
      firstName: "Bob",
      lastName: "Tester",
      email: "bob@example.com",
      phone: "+999121231212",
      location: {
        coord: {
          latitude: 25,
          longitude: 55.1646,
        },
        country: "United Arab Emirates",
        state: "Dubai",
        city: "Dubai",
        line1: "Jumeirah Lake Towers",
        line2: "The Dom Tower, apart 3005",
        zip: "000000",
      },
      slots: slots,
      serviceId: serviceId,
    };
    setBooking(bookingData);
  };

  //   console.log("booking_data", booking_data);

  //   console.log(profile);
  if (slots) {
    return (
      <div className="slots">
        <h1>{slots?.name}</h1>
        <div></div>
        <h2>Slots</h2>
        <div className="vendor-services">
          {slots &&
            slots.map((s, i) => {
              return (
                <div
                  key={s.slotStart}
                  onClick={handlerBooking(s.id, [s.slotStart])}
                >
                  {convertDate(s.slotStart)}
                </div>
              );
            })}
        </div>
      </div>
    );
  }
}

export default Service;
