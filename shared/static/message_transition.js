$(document).ready(() => {


	$(".alert").each(function () {
		const $this = $(this);
		console.log("Setting timeout for message:", $this.text());
		setTimeout(() => {
			console.log("Removing message:", $this.text());
			$this.remove();
		}, 3000);
	});

	$(".messages").on("click", ".btn-close", function () {

		$(this).closest(".alert").remove();
	});
});