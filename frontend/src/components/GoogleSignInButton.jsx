/* global gapi */
import axios from "axios";
import React, { useEffect } from "react";
import { useHistory } from "react-router-dom";

function GoogleSignInButton() {
  const history = useHistory();

  useEffect(() => {
    gapi.signin2.render("g-signin2", {
      theme: "dark",
      width: "block",
      height: "44px",
      longtitle: true,
      scope: "profile email",
      onsuccess: (googleUser) => {
        const id_token = googleUser.getAuthResponse().id_token;
        let tokenFormData = new FormData();
        tokenFormData.set("token", id_token);
        axios({
          method: "post",
          data: tokenFormData,
          url: "http://127.0.0.1:8000/api/buyer/social/",
          headers: { "Content-Type": "multipart/form-data" },
        })
          .then((response) => {
            const token = response.data.token;
            localStorage.setItem("token", token);
            history.push("/");
            window.location.reload();
          })
          .catch((err) => {
            console.log(err.response);
          });
      },
    });
  });

  return (
    <div>
      <div id="g-signin2" />
    </div>
  );
}

export default GoogleSignInButton;
