function popup_tos() {
	const url = "http://localhost:8000/signup/agreement/tos";
	const name = "test";
	const option = "width = 200, height = 500, top = 10, left = 20, location = no";
	window.open(url, name, option);
}