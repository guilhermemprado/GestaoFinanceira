const url_person = "http://127.0.0.1:5000/people"
const url_bank = "http://127.0.0.1:5000/banks"
const url_agency = "http://127.0.0.1:5000/bank_agencies"
const url_account = "http://127.0.0.1:5000/bank_accounts"
const url_moviments = 'http://127.0.0.1:5000/moviments'
const url_moviment = 'http://127.0.0.1:5000/moviment'


const person = document.getElementById("selectNamePerson");
const bank = document.getElementById("selectNameBank");
const agency = document.getElementById("selectNameAgency");
const account = document.getElementById("selectAccountNumber");

const labelIdPerson = document.getElementById("labelIdPerson");
const labelIdBank = document.getElementById("labelIdBank");
const labelIdAgency = document.getElementById("labelIdAgency");
const labelIdAccount = document.getElementById("labelIdAccount");

document.getElementById("selectNamePerson").style.width = "24%";
document.getElementById("selectNameBank").style.width = "24%";
document.getElementById("selectNameAgency").style.width = "24%";
document.getElementById("selectAccountNumber").style.width = "24%";

const onclickPerson = async () => {
    labelIdPerson.textContent = person.value;
}

person.onclick = onclickPerson;

const onclickBank = async () => {
    while (agency.options.length > 0) {
        agency.remove(0);
    }

    labelIdBank.textContent = bank.value;
    await displayOptionAgency();
}

bank.onclick = onclickBank;


const onclickAgency = async () => {
    while (account.options.length > 0) {
        account.remove(0);
    }

    labelIdAgency.textContent = agency.value;
    await displayOptionAccount();
}

agency.onclick = onclickAgency;

const getPostPerson = async () => {
    const response = await fetch(url_person);

    if (response.status !== 200) {
        console.warn('Verifique a url de people, ela retornou o código: ',
            response.status);
        return [];
    }
    const data = await response.json();
    return data;
};

const onclickAccount = async () => {    
    labelIdAccount.textContent = account.value;
}

account.onclick = onclickAccount;

const displayOptionPerson = async () => {
    // Calls the function that gets the data from the person
    const options = await getPostPerson();
    
    // Load the select with the person data
    for (let option of options["Persons"]) {
        const newOption = document.createElement("option");
        newOption.value = option.Id;
        newOption.text = option.Name;
        person.appendChild(newOption);
    }
};

const getPostBank = async () => {
    const response = await fetch(url_bank);

    if (response.status !== 200) {
        console.warn('Verifique a url de banks, ela retornou o código: ',
            response.status);
        return [];
    }
    const data = await response.json();
    return data;
};

const displayOptionBank = async () => {
    // Calls the function that gets the data from the bank
    const options = await getPostBank();
    
    // Load the select with the bank data
    for (let option of options["Banks"]) {
        const newOption = document.createElement("option");
        newOption.value = option.Number;
        newOption.text = option.Name;
        bank.appendChild(newOption);
    }
};

const getPostAgency = async () => {
    const response = await fetch(url_agency);

    if (response.status !== 200) {
        console.warn('Verifique a url de bank_agencies, ela retornou o código: ',
            response.status);
        return [];
    }
    const data = await response.json();
    return data;
};

const displayOptionAgency = async () => {

    // Calls the function that gets the data from the agency
    let dados = await getPostAgency();
    const options = await dados["Banks agencies"].filter(dados => dados.Number_bank.toString() === labelIdBank.textContent);
    
    // First record is always the field name and title, by default
    const newOption = document.createElement("option");
    newOption.text = "Select a agency";
    agency.appendChild(newOption);

    // Load the select with the agency data
    for (let option of options) {
        const newOption = document.createElement("option");
        newOption.value = option.Number_agency;
        newOption.text = option.Name_agency.toString();
        agency.appendChild(newOption);
    }

};

const getPostAccount = async () => {
    const response = await fetch(url_account);

    if (response.status !== 200) {
        console.warn('Verifique a url de account, ela retornou o código: ',
            response.status);
        return [];
    }
    const data = await response.json();
    return data;
};

const displayOptionAccount = async () => {
    // Calls the function that gets the data from the agency
    let dados = await getPostAccount();
    let options = await dados["Banks accounts"].filter(dados => dados.Agency_number.toString() === labelIdAgency.textContent);

    // First record is always the field name and title, by default
    const newOption = document.createElement("option");
    newOption.text = "Select a account";
    account.appendChild(newOption);

    // Load the select with the agency data
    for (let option of options) {
        const newOption = document.createElement("option");
        newOption.value = option.Account;
        newOption.text = option.Account;
        account.appendChild(newOption);
    }
};

const getPostMoviments = async () => {
    const response = await fetch(url_moviments);

    if (response.status !== 200) {
        console.warn('Verifique a url de moviments, ela retornou o código: ',
            response.status);
        return [];
    }
    const data = await response.json();
    return data;
};

const displayOptionMoviments = async () => {
    let table = document.getElementById('tabMoviments');

    // Calls the function that gets the data from the movimentos
    const options = await getPostMoviments();
    const item = options["Moviments"];
    
    for (let index = 0; index < item.length; index++) {
        let newRow = table.insertRow(1);

        let cellId = newRow.insertCell();
        let cellPerson = newRow.insertCell();
        let cellNameBank = newRow.insertCell();
        let cellNameAgency = newRow.insertCell();
        let cellNumberAccount = newRow.insertCell();
        let cellDescription = newRow.insertCell();
        let cellValue = newRow.insertCell();
        let cellDate = newRow.insertCell();
        insertButtonDelete(newRow.insertCell())
        insertButtonUpdate(newRow.insertCell())

        cellId.innerHTML = item[index].Id_moviment;
        cellPerson.innerHTML = item[index].Name_person;
        cellNameBank.innerHTML = item[index].Name_bank;
        cellNameAgency.innerHTML = item[index].Name_agency;
        cellNumberAccount.innerHTML = item[index].Account_number;
        cellDescription.innerHTML = item[index].Description;
        cellValue.innerHTML = item[index].Value;
        cellDate.innerHTML = item[index].Date;
    }
    deleteMoviment();
    BuscaMoviment();
};

const insertButtonDelete = (parent) => {
    let btnDelete = document.createElement("delete");
    let txtDelete = document.createTextNode("\u00D7");
    btnDelete.className = "delete";
    btnDelete.appendChild(txtDelete);
    parent.appendChild(btnDelete);
};

const insertButtonUpdate = (parent) => {
    let btnUpdate = document.createElement("update");
    let txtUpdte = document.createTextNode("\u03BD");
    btnUpdate.className = "update";
    btnUpdate.appendChild(txtUpdte);
    parent.appendChild(btnUpdate);
};

const btnClickAdicionar = async () => {
    let selDescription = document.getElementById("inpDescription").value;
    let selValue = document.getElementById("inpValue").value;
    let selDate = document.getElementById("inpDate").value;

    if (isNaN(labelIdPerson.textContent)) {
        alert("Selecione uma pessoa na lista!");
    } else if (isNaN(labelIdBank.textContent)) {
        alert("Selecione um banco na lista!");
    } else if (isNaN(labelIdAgency.textContent)) {
        alert("Selecione uma agência na lista!");
    } else if (isNaN(labelIdAccount.textContent)) {
        alert("Selecione uma conta na lista!");
    } else if (selDescription == "") {
        alert("Informe uma descrição!");
    } else if (isNaN(selValue)) {
        alert("Valor informado não e valido!");
    } else if (selDate == "") {
        alert("Informe uma data válida!");
    } else {
        if (Number(labelIdMoviment.textContent) === 0) {

            await postMoviment(0, labelIdAccount.textContent, selDescription, selValue, selDate)
            window.location.reload(true);
            alert("Movimento adicionado com sucesso!")
        } else {
            if (confirm("Deseja realmente alterar o movimento?")) {
                await postMoviment(labelIdMoviment.textContent, labelIdAccount.textContent, selDescription, selValue, selDate)
                window.location.reload(true);
                alert("Movimento alterado com sucesso!")
            };
            window.location.reload(true);
        };
    }
}

async function postMoviment(inputIdMovimento, inputIdAccount, inputDescription, inputValue, inputDate) {
    const formData = new FormData();
    formData.append('account_number', inputIdAccount);
    formData.append('description', inputDescription);
    formData.append('value', inputValue);
    formData.append('date', inputDate);

    if (Number(inputIdMovimento) === 0) {
        console.log(inputIdAccount, ":,",inputDescription, ":,",inputValue, ":,",inputDate)
        fetch(url_moviment, {
            method: 'post',
            body: formData,
        });
    } else {
        fetch("http://127.0.0.1:5000/update_moviment?id=" + inputIdMovimento, {
            method: 'post',
            body: formData,
        });
    };
};

const BuscaMoviment = async () => {
    let labelIdCar = document.getElementById("labelIdMoviment");
    let update = document.getElementsByClassName("update");

    let i;
    for (i = 0; i < update.length; i++) {
        update[i].onclick = async function () {
            let div = this.parentElement.parentElement;
            const idMoviment = div.getElementsByTagName('td')[0].innerHTML;

            labelIdMoviment.textContent = idMoviment;

            selectdUpdatePerson(div);

            selectdUpdateBank(div);
            await onclickAgency();

            selectdUpdateAgency(div);
            await onclickAccount();

            selectdUpdateAccount(div);

            document.getElementById("inpDescription").value = div.getElementsByTagName('td')[5].innerHTML
            document.getElementById("inpValue").value = div.getElementsByTagName('td')[6].innerHTML
            document.getElementById("inpDate").value = div.getElementsByTagName('td')[7].innerHTML

        };
    };
};

const selectdUpdatePerson = (objeto) => {
    let select = document.querySelector('#selectNamePerson');
    for (let iLine = 0; iLine < select.options.length; iLine++) {
        if (select.options[iLine].text === objeto.getElementsByTagName('td')[1].innerHTML) {
            select.selectedIndex = iLine;
            break;
        };
    };
};

const selectdUpdateBank = (objeto) => {
    let select = document.querySelector('#selectNameBank');
    for (let iLine = 0; iLine < select.options.length; iLine++) {
        if (select.options[iLine].text === objeto.getElementsByTagName('td')[2].innerHTML) {
            select.selectedIndex = iLine;
            break;
        };
    };
    onclickBank();
};

const selectdUpdateAgency = (objeto) => {
    let select = document.querySelector('#selectNameAgency');
    for (let iLine = 0; iLine < select.options.length; iLine++) {
        if (select.options[iLine].text === objeto.getElementsByTagName('td')[3].innerHTML) {
            select.selectedIndex = iLine;
            break;
        };
    };
    onclickAgency();
};

const selectdUpdateAccount = (objeto) => {
    let select = document.querySelector('#selectAccountNumber');
    for (let iLine = 0; iLine < select.options.length; iLine++) {
        if (select.options[iLine].text === objeto.getElementsByTagName('td')[4].innerHTML) {
            select.selectedIndex = iLine;
            break;
        };
    };
    onclickAccount();
};

const deleteItem = (item) => {
    fetch(url_moviment + '?id=' + item, {
        method: 'delete'
    });
};

const deleteMoviment = () => {
    let close = document.getElementsByClassName("delete");

    let i;
    for (i = 0; i < close.length; i++) {
        close[i].onclick = function () {
            let div = this.parentElement.parentElement;
            const nomeItem = div.getElementsByTagName('td')[0].innerHTML
            if (confirm("Você tem certeza?")) {
                div.remove()
                deleteItem(nomeItem)
                alert("Movimento removido!")
            };
        };
    };
};

displayOptionPerson();
displayOptionBank();
displayOptionAgency();
displayOptionAccount();
displayOptionMoviments();