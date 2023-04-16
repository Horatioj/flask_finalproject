$(document).ready(function () {
    // Define function to perform search
    function doSearch() {
        // Construct URL for AJAX request
        const url = '/SearchFilter';
        // Get form data
        const data = $('form').serialize();
        // Send AJAX request
        $.post(url, data)
            .done(function (response) {
                // Update search results
                $('#results').html(response);
            })
            .fail(function (error) {
                console.log(error);
            });
    }

    // Send AJAX request when search form is submitted
    $('form').on('submit', function (event) {
        // Prevent default form submission
        event.preventDefault();
        // Perform search
        doSearch();
    });

    // Send AJAX request when category checkbox is clicked
    $('input[type=checkbox][name=category]').change(function () {
        // Get category value
        const category = $(this).val();
        // Check if checkbox is checked
        if ($(this).is(':checked')) {
            // Perform filter
            doSearch(category);
        } else {
            // Perform filter for All categories
            doSearch('All');
        }

        // Send AJAX request when sorting option is selected
        $('select[name=sort]').change(function () {
            // Perform search with selected sorting header
            doSearch();
        });


        // Define function to clear search results
        function clearResults() {
            $('#results').html('');
        }

        // Clear search results when reset button is clicked
        $('input[type=reset]').on('click', function () {
            clearResults();
        });
    });
});



