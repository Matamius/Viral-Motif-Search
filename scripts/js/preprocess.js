// run when page ready
$(document).ready(function () {
	// handle form submission to prevent default form submission
	$("#uploadForm").submit(function (e) {
		e.preventDefault(); 

		// get fasta and validate extension
		const fileInput = $("#fileInput")[0].files[0];
		if (!fileInput) {
			alert("Please select a FASTA file to upload.");
			return;
		}
		const validExtension = ['fasta', 'fa', 'txt'];
		const fileName = fileInput.name.toLowerCase();
		const fileExtension = fileName.split('.').pop();

		if (!validExtension.includes(fileExtension)){
			$("#fileError").show()
			return;
		} else {
			$("#fileError").hide()
		}
		
		// create formData for matches key:value for file and filedata
		const formData = new FormData();
		formData.append("file", fileInput);

		// backend process
		$.ajax({
			url: "../bin/pieced_together.cgi", 
			type: "POST", 
			data: formData,
			processData: false,
			contentType: false,
			dataType: 'json',
			beforeSend: function () {
				// added loading icon
				$("#loadingIndicator").show();
			},
			success: function (data) {
				// hide loading and clear previous results, if applicable
				$("#loadingIndicator").hide();
				$("#results").show();
				$("#summary").empty();
				$("#summarized_results").show();
				if ($("#resultsTableBody").length > 0) {
					$("#resultsTableBody").find(".flex-row").remove();
				}
				
				// unique pattern ids
				const summaryFrameIds = {};
				
				// populate results table
				if (data.matches && data.matches.length > 0) {
					data.matches.forEach(match => {
						// new set for each frame
						if (!summaryFrameIds[match.frame]) {
							summaryFrameIds[match.frame] = new Set(); 
						}
						summaryFrameIds[match.frame].add(match.regex_id);
						
						const row = `<div class="flex-row">
			                                <div class="flex-cell">${match.frame}</div>
			                                <div class="flex-cell">${match.peptide}</div>
			                                <div class="flex-cell">${match.regex_id}</div>
			                                <div class="flex-cell">${match.regex_sitename}</div>
			                                <div class="flex-cell">${match.regex_descr}</div>
			                                <div class="flex-cell"><code>${match.regex_pattern}</code></div>
		                           	</div>`;
						$("#resultsTableBody").append(row);
					});
					
					// generate an array and count of unique ids for each frame
					let summaryResult = `From your file, "${fileInput.name}", there are potentially:<br><br>`;
					Object.keys(summaryFrameIds).forEach(frame => {
                        			const uniqueIdsArray = Array.from(summaryFrameIds[frame]);
						const uIdCount = uniqueIdsArray.length;
						const uniqueIds = uniqueIdsArray.join('<br>');
						// create drop down for summarized results
			                        summaryResult += `There are potentially <strong>${uIdCount}</strong> motif matches in <strong>frame ${frame}</strong>
								<button class="expandButton" data-frame="${frame}">Show Unique IDs</button>
			                        		<div class="uniqueIdsExpanded" id="frame-${frame}" style="display:none;">
			                           			${uniqueIds}
			                       			</div><br><br>`;
			                });

			                $("#summary").html(summaryResult);
			        }
				else {
					alert("No matches found.");
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				$("#loadingIndicator").hide();
				console.error("AJAX Error:", {
					status: jqXHR.status,
					statusText: jqXHR.statusText,
					responseText: jqXHR.responseText,
					error: errorThrown
				});
				alert("An error occurred while processing the file.");
			}
		});
	});
		// toggle for info dump button
	$(document).on('click', '.expandButton', function () {
        	const frameId = $(this).data('frame');
        	const content = $(`#frame-${frameId}`);
        	content.toggle(); 
    	});
});
