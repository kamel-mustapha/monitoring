function show_alert(messages, color = "#374151") {
  let message_overlay = document.getElementById("message_overlay");
  message_overlay.querySelector(".hide").click();

  message_overlay.querySelector("ul").innerHTML = "";

  if (typeof messages == "string") {
    let list_element = document.createElement("li");
    list_element.innerHTML = messages;
    message_overlay.querySelector("ul").appendChild(list_element);
  } else {
    for (let message of messages) {
      let list_element = document.createElement("li");
      list_element.innerHTML = `* ${message}`;
      message_overlay.querySelector("ul").appendChild(list_element);
    }
  }
  message_overlay.style.color = color;

  message_overlay.querySelector(".show").click();

  setTimeout(() => {
    message_overlay.querySelector(".hide").click();
  }, 10000);
}

function get_form_values(form) {
  let data = {};
  let form_inputs = Array.from(form.querySelectorAll("input"));
  for (let input of form_inputs) {
    data[input.name] = input.value;
  }
  return data;
}

function register_or_login(event, elem, register = false) {
  event.preventDefault();
  let user_data = get_form_values(elem);
  fetch(
    register ? "/register/" : "/login/",
    (options = {
      method: "POST",
      body: JSON.stringify(user_data),
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
      },
    })
  )
    .then((res) => res.json())
    .then((data) => {
      if (data.status && data.status == "success") {
        show_alert(data.message, "#15803d");
        setTimeout(() => {
          if (register) {
            window.location.replace("/activation/");
          } else {
            window.location.replace("/");
          }
        }, 2000);
      } else if (data.errors) {
        show_alert(data.errors, "#b91c1c");
      } else if (data.message) {
        show_alert(data.message, "#b91c1c");
      }
    });
}
