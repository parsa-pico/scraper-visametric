import json


def get_date(code, consular_id):
    return """var http = new XMLHttpRequest();
            var url =
            "https://ir-appointment.visametric.com/ir/appointment-form/personal/getdate";
            var code = """+f"'{code}'"+""";
            var params =
            "consularid="""+str(consular_id)+"""&exitid=1&servicetypeid=1&calendarType=2&totalperson=1&mailConfirmCode=" + code;
            http.open("POST", url, true);

            http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            http.setRequestHeader(
            "X-Csrf-Token",
             $('meta[name="csrf-token"]').attr("content")
            );
            http.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            http.onreadystatechange = function () {
            let copy_right_element = document.getElementsByClassName("copyright")[0];
            if (http.readyState == 4 && http.status == 200) {
                copy_right_element.innerHTML = http.responseText;
            } else {
                copy_right_element.innerHTML = "error " + http.responseText;
            }
            };
            http.send(params);
            """


def stop_timer():
    return (
        """
    const highestId = window.setTimeout(() => {
    for (let i = highestId; i >= 0; i--) {
    window.clearInterval(i);
            }
        }, 0);
    """)


def get_date_edit_page():
    return """var http = new XMLHttpRequest();
var url = 'https://ir-appointment.visametric.com/ir/editappointment/get-date';

http.open('POST', url, true);

http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
http.setRequestHeader(
  "X-Csrf-Token",
  $('meta[name="csrf-token"]').attr("content")
);
http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

http.onreadystatechange = function () {
  let copy_right_element = document.getElementsByClassName("copyright")[0];
  if (http.readyState == 4 && http.status == 200) {
    copy_right_element.innerHTML = http.responseText;
  } else {
    copy_right_element.innerHTML = "error " + http.responseText;
  }
}
http.send();
"""


def enable_dates(dates):
    return f"var open_dates={dates}" + """ 
document.addEventListener("click", someFunction);
var monthes={july:"07",august:"08",september:"09",october:"10"}

function someFunction(event) {
const event_class=event.target.className.toString();
  if (event_class=="next" || event_class=="prev" || event_class.includes("calendarinput") ){
      current_month=document
      .querySelectorAll(".datepicker-days .datepicker-switch")[0].textContent.toString();
      current_month=monthes[Object.keys(monthes).find(m=>current_month.toLowerCase().includes(m))];
      current_month_dates=open_dates.filter(d=>d.month==current_month);
      current_month_dates.forEach(d=>{
        var day=parseInt(d.day)
        var days=[...document.querySelectorAll(".datepicker-days td")]
        var open_date=days.filter(d=>d.textContent.toString().trim()==day && !d.classList.contains("old")&& !d.classList.contains("new"))[0]
        open_date.classList.remove("disabled")});
  }
}
"""


def remove_animations():
    return """
    const addCSS = css => document.head.appendChild(document.createElement("style")).innerHTML=css;
    addCSS(`*, *:before, *:after {
     -webkit-transition: none !important;
     -moz-transition: none !important;
     -ms-transition: none !important;
     -o-transition: none !important;        
     transition: none !important;

     -webkit-transform: none !important;
     -moz-transform: none !important;
     -ms-transform: none !important;
     -o-transform: none !important;        
     transform: none !important;
    }`);
    """


def fill_form(info):
    info = json.dumps(info)
    return """
// fill form page
function fill_input(key, value, by = "name") {
  let e = null;
  switch (by) {
    case "name":
      e = document.getElementsByName(key)[0];
      break;
    case "id":
      e = document.getElementById(key);
      break;
    case "class":
      e = document.getElementsByClassName(key)[0];
      break;
    case "tag":
      e = document.getElementsByTagName(key)[0];
      break;
    default:
      e = document.getElementsByName(key)[0];
  }
  e.value = value;
}

function fill_select(id, value) {
  const selectElement = document.getElementById(id);
  const options = selectElement.options;
  for (let i = 0; i < options.length; i++) {
    if (options[i].value === value) {
      options[i].selected = true;
      break;
    }
  }
}

function fill_form(person_index, person_info) {
  fill_input(`name${person_index + 1}`, person_info["first_name"]);
  fill_input(`surname${person_index + 1}`, person_info["last_name"]);
  fill_input(`passport${person_index + 1}`, person_info["passport_number"]);
  fill_input(`phone${person_index + 1}`, person_info["phone_number"]);
  if (person_info["phone_number_emg"] !== "-") {
    fill_input(`phone2${person_index + 1}`, person_info["phone_number_emg"]);
  }
  fill_input(`email${person_index + 1}`, person_info["email"]);
  fill_select(`birthyear${person_index + 1}`, person_info["birth"]["year"]);
  fill_select(`birthmonth${person_index + 1}`, person_info["birth"]["month"]);
  fill_select(`birthday${person_index + 1}`, person_info["birth"]["day"]);
}

var info =""" + info+"""
fill_input("sheba_number", info["generic_info"]["sheba"]);
fill_input("sheba_name", info["generic_info"]["persian_name"]);
for (let i = 0; i < info["persons_info"].length; i++) {
  info["persons_info"][i]["email"] = info["generic_info"]["email"];
  fill_form(i, info["persons_info"][i]);
}



"""
