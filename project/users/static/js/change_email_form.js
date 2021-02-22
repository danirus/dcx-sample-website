const confirm_email_msg = gettext("A confirmation request has been sent to your new email address.");

class ChangeEmailForm {
  constructor() {
    this.form = document.getElementById("emailform");
    this.help = document.getElementById("emailhelp");
    this.initial = {
      csrfmiddlewaretoken: this.form.elements['csrfmiddlewaretoken'].value,
      email: this.form.elements['email'].value
    }
  }

  post(_) {
    let fields = {
      csrfmiddlewaretoken: this.form.elements['csrfmiddlewaretoken'].value,
      email: this.form.elements['email'].value
    }
    // If email didn't change since the page was loaded there is no
    // need to submit the form. Just inform the user about the fact.
    if (fields['email'] === this.initial['email']) {
      this.help.textContent = gettext("The email address has not changed.");
      this.help.classList.remove("hide");
      this.help.classList.add("text-info");
      return false;
    }

    let formBody = [];
    for (const field in fields) {
      let key = encodeURIComponent(field);
      let value = encodeURIComponent(fields[field]);
      formBody.push(`${key}=${value}`);
    }
    formBody = formBody.join("&");
    fetch('/user/account/edit/email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset-UTF-8',
      },
      body: formBody
    }).then(response => {
      if (response.status == 200) {
        return response.json();
      }
    }).then(data => {
      if (data.status == "success") {
        this.help.textContent = confirm_email_msg;
        this.help.classList.remove("hide");
        this.help.classList.add("text-success");
      } else if (data.status == "error") {
        this.help.textContent = data.errors.email[0];
        this.help.classList.remove("hide");
        this.help.classList.add("text-error");
      }
    });
    return false;  // To prevent calling the action attribute.
  }

}

let change_email_form = null;

window.addEventListener("DOMContentLoaded", (_) => {
  change_email_form = new ChangeEmailForm();
});