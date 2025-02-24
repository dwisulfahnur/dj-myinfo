async function authorize() {
  const res = await fetch("/api/authorize", {
    method: "POST",
    headers: { "X-CSRFToken": window.CSRF_TOKEN },
  })
  const data = await res.json()
  const authorizeUrl = data.authorize_url
  window.location = authorizeUrl;
}

async function getPersonData(code) {
  const res = await fetch('/api/persons', {
    method: 'POST',
    body: JSON.stringify({ code }),
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN,
      "Content-Type": "application/json",
    },
  })
  return res
}

async function handleFormSubmit(evt) {
  evt.preventDefault()
  const fields = [
    "uinfin", "fullname", "sex", "race", "nationality", "dob", "email",
    "mobileno", "regaddress", "housingtype", "marital", "edulevel", "edulevel",
  ]
}

function formatAddress(data) {
  const parts = [];
  
  if (data.unit?.value) parts.push(`Unit ${data.unit.value}`);
  if (data.floor?.value) parts.push(`Floor ${data.floor.value}`);
  if (data.block?.value) parts.push(`Block ${data.block.value}`);
  if (data.street?.value) parts.push(data.street.value);
  if (data.building?.value) parts.push(data.building.value);
  if (data.postal?.value) parts.push(`Postal ${data.postal.value}`);
  if (data.country?.desc) parts.push(data.country.desc);
  
  return parts.filter(Boolean).join(", ");
}

function formatMobilNo(mobileno){
  return `${mobileno.prefix.value}${mobileno.areacode.value}${mobileno.nbr.value}`
}


function populateForm(data) {
  document.querySelector("[name='uinfin']").value = data.uinfin.value;
  document.querySelector("[name='name']").value = data.name.value;
  document.querySelector("[name='dob']").value = data.dob.value;
  document.querySelector("[name='birthcountry']").value = data.birthcountry.desc;
  document.querySelector("[name='sex']").value = data.sex.desc;
  document.querySelector("[name='race']").value = data.race.desc;
  document.querySelector("[name='nationality']").value = data.nationality.desc;
  document.querySelector("[name='email']").value = data.email.value;
  document.querySelector("[name='mobileno']").value = formatMobilNo(data.mobileno);
  document.querySelector("[name='regadd']").value = formatAddress(data.regadd);
  document.querySelector("[name='housingtype']").value = data.housingtype.desc;
  document.querySelector("[name='hdbtype']").value = data.hdbtype.desc;


  document.querySelector("[name='employmentsector']").value = data.employmentsector.value;
  document.querySelector("[name='occupation']").value = data.occupation.value;
  document.querySelector("[name='marital']").value = data.marital.desc;

  let incomeDiv = document.getElementById("income-history");
  incomeDiv.innerHTML = "";

  data.noahistory.noas.forEach((entry, index) => {
    let incomeEntry = document.createElement("div");
    incomeEntry.classList.add("mb-3", "col-md-6", "income-entry");
    incomeEntry.innerHTML = `
            <label class="form-label">Annual Income (${entry.yearofassessment.value})</label>
            <input type="text" name="income_${index}" class="form-control income-amount" value="$${entry.amount.value.toLocaleString()}" disabled>
        `;
    incomeDiv.appendChild(incomeEntry);
  });

  let cpfDiv = document.getElementById("cpf-history");
  cpfDiv.innerHTML = "";
  data.cpfcontributions.history.forEach((entry, index) => {
    let cpfEntry = document.createElement("div");
    cpfEntry.classList.add("mb-3", "col-md-4", "cpf-entry");
    cpfEntry.innerHTML = `
      <label class="form-label">CPF Contribution (${entry.month.value})</label>
      <input type="text" name="cpf_${index}" class="form-control cpf-amount" value="${entry.amount.value}" disabled>
      <small class="form-text text-muted cpf-month">${entry.month.value}</small>
      <small class="form-text text-muted cpf-employer">Employer: ${entry.employer.value}</small>
    `;
    cpfDiv.appendChild(cpfEntry);
  });

  let noaDiv = document.getElementById("noa-history");
  noaDiv.innerHTML = "";
  data.noahistory.noas.forEach(function (noa, index) {
    let noaEntry = document.createElement('div');
    noaEntry.classList.add("row", "align-items-center", "mb-3", "col-md-12", "noa-entry");
    noaEntry.innerHTML = `
      <div class="col-md-1">
        <label class="form-label">Year</label>
        <input value="${noa.yearofassessment.value}" class="form-control" disabled />
      </div>
      <div class="col-md-3">
        <label class="form-label">Value</label>
        <input value="${noa.amount.value}" class="form-control" disabled />
      </div>
      <div class="col-md-2">
        <label class="form-label">Employment</label>
        <input value="${noa.employment.value}" class="form-control" disabled />
      </div>
      <div class="col-md-2">
        <label class="form-label">Trade</label>
        <input value="${noa.trade.value}" class="form-control" disabled />
      </div>
      <div class="col-md-2">
        <label class="form-label">Rent</label>
        <input value="${noa.rent.value}" class="form-control" disabled />
      </div>
      <div class="col-md-2">
        <label class="form-label">Interest</label>
        <input value="${noa.interest.value}" class="form-control" disabled />
      </div>
    `;
    noaDiv.appendChild(noaEntry)
  })
}

document.addEventListener("DOMContentLoaded", function () {
  (async function () {
    const authorizeButtons = document.querySelectorAll("#authorize-btn1,#authorize-btn2");
    authorizeButtons.forEach(btn => {
      btn.addEventListener("click", function () {
        console.log("authorize...")
        authorize()
      })
    })

    const form = document.querySelector("form#form-submit");
    const isCallbackPage = window.location.href.indexOf("callback?code") > -1;
    if (isCallbackPage) {
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');
      if (code) {
        getPersonData(code).then(res => {
          document.getElementById("loading-container").classList.add('d-none')
          if (res.status === 200) {
            res.json().then(data => {
              document.getElementById("form-container").classList.remove('d-none')
              populateForm(data)
            })
          } else {
            document.getElementById("error-container").classList.remove('d-none')
          }
        })
      }
      if (!!form) {
        form.addEventListener("submit", handleFormSubmit);
      }
    }
  })()
})
