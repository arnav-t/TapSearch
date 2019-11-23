function populateList(data) {
	var list = $('#res');
	list.empty();
	var i;
	for (i = 0; i < data.length; ++i) {
		var li = $('<li/>').text(data[i]).appendTo(list);
	}
}

function getAll() {
	$.get('/api/get',
	function(data, status) {
		if (status === "success") {
			populateList(data);
		}
	});
}

$('#add-btn').click(function() {
	$.post("/api/add",
	JSON.stringify({
		data: $('#add-txt').val()
	}),
	function(data, status) {
		populateList(data);
	}, "json");
});

$('#idx-btn').click(function() {
	var url;
	var id = parseInt($('#idx-txt').val());
	if (!isNaN(id)) {
		url = `/api/index?id=${id}`
	}
	else {
		url = `/api/index`
	}
	$.get(url,
	function(data, status) {
		if (status === "success") {
			alert("Paragraph(s) Indexed successfully!");
		}
		else {
			alert("Error! Please check the index.")
		}
	});
});

$('#search-btn').click(function() {
	$.get(`/api/search?query=${$('#search-txt').val()}`,
	function(data, status) {
		if (status === "success") {
			populateList(data);
		}
	});
});

$('#clear-btn').click(function() {
	$.get('/api/clear',
	function(data, status) {
		if (status === "success") {
			alert("Memory cleared successfully!");
		}
	});
});

getAll();

$('#view-btn').click(getAll);

function readPDF() {
    var file = document.getElementById('file-in').files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var content = e.target.result;
			var getText = function(content) {
				return pdfjsLib.getDocument({data: content}).then(function(pdf) {
					var pages = [];
					for (var i = 0; i < pdf.numPages; i++) {
						pages.push(i);
					}
					return Promise.all(pages.map(function(pageNumber) {
						return pdf.getPage(pageNumber + 1).then(function(page) {
							return page.getTextContent().then(function(textContent) {
								return textContent.items.map(function(item) {
									return item.str;
								}).join(' ');
							});
						});
					})).then(function(pages) {
						return pages.join("\n\n");
					});
				}).then(function(result) {
					$.post("/api/add",
					JSON.stringify({
						data: result
					}),
					function(data, status) {
						populateList(data);
					}, "json");
				});
			}
			getText(content);
			
        }
        reader.readAsText(file);
    }
}