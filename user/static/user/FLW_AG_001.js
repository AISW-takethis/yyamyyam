function popup_age() {
	const url = "http://localhost:8000/signup/agreement/age";
	const name = "test";
	const option = "width = 200, height = 500, top = 10, left = 20, location = no";
	window.open(url, name, option);
}

function popup_tos() {
	const url = "http://localhost:8000/signup/agreement/tos";
	const name = "test";
	const option = "width = 200, height = 500, top = 10, left = 20, location = no";
	window.open(url, name, option);
}

function popup_pp() {
	const url = "http://localhost:8000/signup/agreement/pp";
	const name = "test";
	const option = "width = 200, height = 500, top = 10, left = 20, location = no";
	window.open(url, name, option);
}

function popup_mc() {
	const url = "http://localhost:8000/signup/agreement/mc";
	const name = "test";
	const option = "width = 200, height = 500, top = 10, left = 20, location = no";
	window.open(url, name, option);
}


function check_essential() {
	const f = document.agreement_form;
	if (f.agree_age.checked === false || f.agree_tos.checked === false || f.agree_pp.checked === false) {
		alert('필수 항목에 체크해 주세요.');
	} else {
		alert('통과');
		// f.submit();
	}
}