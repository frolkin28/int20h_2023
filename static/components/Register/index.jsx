import React, { useState } from "react";
import { Link, useHistory } from "react-router-dom";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState(null);
  const history = useHistory();

  const onSubmit = (e) => {
    e.preventDefault();
    console.log(email, password);
    if (!(email && password && firstName && lastName)) {
      setError("Fill all fields");
      return;
    }
    fetch("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        email: email,
        password: password,
        first_name: firstName,
        last_name: lastName,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data?.status === "success") history.push("/");
        else setError(JSON.stringify(error));
      });
  };

  return (
    <section className="home-page vh-100">
      <div className="container-fluid h-custom">
        <div className="row d-flex justify-content-center align-items-center h-100">
          <div className="col-md-9 col-lg-6 col-xl-5">
            <img
              src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
              className="img-fluid"
              alt="Sample image"
            />
          </div>
          <div className="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
            <form onSubmit={onSubmit}>
              <div class="divider d-flex align-items-center my-4">
                <h3 class="text-center fw-bold mb-0">Register</h3>
              </div>

              {error && (
                <div class="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              <div className="form-outline mb-4">
                <label className="form-label" for="email">
                  Email address
                </label>
                <input
                  id="email"
                  className="email form-control form-control-lg"
                  placeholder="Enter a valid email address"
                  onChange={(e) => {
                    setEmail(e.target.value);
                  }}
                />
              </div>

              <div className="form-outline mb-4">
                <label className="form-label" for="first-name">
                  First name
                </label>
                <input
                  id="first-name"
                  type="text"
                  className="form-control form-control-lg"
                  placeholder="Enter first name"
                  onChange={(e) => {
                    setFirstName(e.target.value);
                  }}
                />
              </div>

              <div className="form-outline mb-4">
                <label className="form-label" for="last-name">
                  Last name
                </label>
                <input
                  id="last-name"
                  type="text"
                  className="form-control form-control-lg"
                  placeholder="Enter last name"
                  onChange={(e) => {
                    setLastName(e.target.value);
                  }}
                />
              </div>

              <div className="form-outline mb-3">
                <label className="form-label" for="password">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  className="form-control form-control-lg"
                  placeholder="Enter password"
                  onChange={(e) => {
                    setPassword(e.target.value);
                  }}
                />
              </div>

              <div className="text-center text-lg-start mt-4 pt-2">
                <button
                  type="submit"
                  className="btn btn-primary btn-lg"
                  style={{
                    paddingLeft: "2.5rem",
                    paddingRight: "2.5rem",
                  }}
                >
                  Register
                </button>
                <p className="small fw-bold mt-2 pt-1 mb-0">
                  Already have an account?
                  <Link
                    className="link-danger"
                    to={"/login"}
                    style={{
                      margin: "5px",
                    }}
                  >
                    Login
                  </Link>
                </p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Register;
