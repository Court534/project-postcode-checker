// use jquery to retrieve crimes in the area, primary care trust, nearest postcodes, planning permission records from an api and populate it into correct boxes
$(document).ready(function() {
    
    $("button").on("click", function(e){
        e.preventDefault();
        var postcode = $("#postcode").val();
        var url_to_query = "https://hfv17k6l60.execute-api.us-east-1.amazonaws.com/cs-project?postcode=" + postcode
        alert("Now searching for postcode: " + postcode);

        $.get(url_to_query, function(data, status){
            console.log(data, status)
            data = JSON.parse(data)
                
            const crime = data.crime_stats
            const pct = data.parliamentary_constituency
            const planning = data.plan_perm
            const nearest = data.nearby_postcodes

            console.log(crime)

            // Outputting crime data in a more readable format
            const crimeResults = crime.map(item => {
                return `<p>${item[0]}, <span>${item[1]}</span> </p>`;
            }).join('');
            
            console.log(crimeResults)
            console.log(nearest)
            console.log(JSON.stringify(planning[0]))

            //  Outputting near postcode data in a more readable format
            const nearestResults = nearest.map(item => {
                return `<p>${item}</p>`;
            })

            // Outputting planning permission data in text removing everything else
            const planningResults = planning.map(planning => {
                return `<p>${JSON.stringify(planning)}</p>`;
            })
            

            $("#crimes_id").html(crimeResults)
            $("#pct_id").html(pct)
            $("#planning_perm_id").html(planningResults)
            $("#near_postcodes_id").html(nearestResults)
        });
    });
});
