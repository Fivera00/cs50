document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);
  // Send an email!
  document
    .querySelector("#compose-form")
    .addEventListener("submit", send_email);

  load_mailbox("inbox");
  // By default, load the inbox
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#email-open").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function send_email(event) {
  // Collect data
  event.preventDefault();
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value,
    }),
  }).then((response) => load_mailbox("sent"));
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-open").style.display = "none";

  // Show the mailbox name
  document.querySelector("#heading").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;
  //Have to clean the inside first, otherwise the html will stay
  document.querySelector("#emails-preview").innerHTML = "";

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((data) => {
      data.forEach((element) => {
        // validate event
        const inbox_item = document.createElement("tr");
        inbox_item.style.cursor = "pointer";
        inbox_item.addEventListener("click", (e) => {
          if (e.target.tagName === "TD") {
            load_email(element.id);
          } else {
            archive_email(element.id, element.archived);
          }
        });

        if (mailbox === "sent") {
          inbox_item.innerHTML =
            `<td class="name">${element["sender"]}</td>` +
            `<td class="subject">${element["subject"]}</td>` +
            `<td class="time">${element["timestamp"]}</td>`;
        } else {
          inbox_item.innerHTML =
            `
          <td class="name">${element["sender"]}</td>` +
            `<td class="subject">${element["subject"]}</td>` +
            `<td class="time">${element["timestamp"]}</td>` +
            `<td><button type="button" class="btn btn-sm    btn-outline-primary"> </button></td>`;
        }

        // coloring read emails
        if (element.read) {
          inbox_item.className = "table-secondary";
        }

        inbox_item.querySelectorAll("button").forEach((a_item) => {
          a_item.innerText = element.archived ? "Unarchive" : "Archive";
        });
        // appending it in the table in HTML
        document.querySelector("#emails-preview").appendChild(inbox_item);
      });
    });
}

function load_email(id) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      // Show only the email
      document.querySelector("#emails-view").style.display = "none";
      document.querySelector("#compose-view").style.display = "none";
      document.querySelector("#email-open").style.display = "block";

      // elements needed for the html code
      const div_info = document.createElement("div");
      const div_body = document.createElement("div");
      const div_buttons = document.createElement("div");
      div_info.className = "email-info";

      // emptying the email page first
      document.querySelector("#email-open").innerHTML = "";
      // Archive and reply button
      const archive = document.createElement("button");
      archive.innerText = email.archived ? "Unarchive" : "Archive";
      archive.className = "btn btn-sm btn-outline-secondary archive";

      const emailOwner = document.getElementById("email-owner").innerHTML;
      const emailSender = email["sender"];

      if (emailOwner != emailSender) {
        const reply = document.createElement("button");
        reply.innerText = "Reply";
        reply.className = "btn btn-sm btn-outline-secondary reply";
        reply.addEventListener("click", () => reply_email(email.id));
        div_buttons.appendChild(reply);
      }

      // event listener for the buttons
      archive.addEventListener("click", () =>
        archive_email(email.id, email.archived)
      );

      // body and details html
      div_info.innerHTML =
        `<p><b>From:</b> ${email.sender}</p>` +
        `<p><b>To:</b> ${email.recipients}</p>` +
        `<p><b>Subject:</b> ${email.subject}</p>` +
        `<p><b>Timestamp:</b> ${email.timestamp}</p>`;
      div_body.innerHTML = `<hr><p>${email.body}</p>`;

      // Mark as read button if the email is unread
      if (email.read) {
        read = document.createElement("button");
        read.className = "btn btn-sm btn-outline-secondary ready";
        read.innerHTML = "Mark as Unread";
        read.addEventListener("click", function () {
          fetch("/emails/" + email["id"], {
            method: "PUT",
            body: JSON.stringify({ read: false }),
          }).then((response) => load_mailbox("inbox"));
        });
        div_buttons.appendChild(read);
      }

      // adding it the content
      div_buttons.appendChild(archive);
      document.querySelector("#email-open").appendChild(div_info);
      document.querySelector("#email-open").appendChild(div_buttons);
      document.querySelector("#email-open").appendChild(div_body);
    });

  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

function archive_email(id, archive_status) {
  // archiving unarchived
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !archive_status,
    }),
  }).then(() => load_mailbox("inbox"));
}

function reply_email(id) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      compose_email();
      // filling the form with the right info
      document.querySelector("#compose-recipients").value = email["sender"];
      if (email.subject.startsWith("Re: "))
        document.querySelector("#compose-subject").value = email["subject"];
      else
        document.querySelector("#compose-subject").value =
          "Re: " + email["subject"];
      let content = `
      On ${email["timestamp"]}, ${email["sender"]} wrote: ${email["body"]} ;
    `;
      document.querySelector("#compose-body").value = content;
    });
}
