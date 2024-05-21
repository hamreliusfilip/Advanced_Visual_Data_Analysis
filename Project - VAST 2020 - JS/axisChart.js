function createAxisChart(dataURL) {

    function convertTimestamp(timestamp) {
        // Convert seconds to milliseconds
        var milliseconds = timestamp * 1000;

        // Subtract milliseconds from 12:00 AM Jan. 1, 2025
        var date = new Date(2025, 0, 1); // Jan is 0 in JavaScript
        date.setTime(date.getTime() - milliseconds);

        // Format the date in ISO 8601 format
        return date.toISOString();
    }

    d3.csv(dataURL).then(function (data) {
        var nodes = [];

        data.forEach(function (d) {
            if (d.eType != 5) {
                if (d.Time >= 0) { // Check if the time is non-negative
                    var sourceNode = { id: d.Source, target: d.Target, eType: d.eType, time: convertTimestamp(d.Time) };
                    nodes.push(sourceNode);
                }

            }
        });

        const width = 1000;
        const marginTop = 20;
        const marginRight = 20;
        const marginBottom = 30;
        const marginLeft = 50;
        const rowHeight = 2;
        const height = rowHeight * nodes.length + marginTop + marginBottom;

        let tooltipVisible = false;
        let selectedNode = null;

        // Count the frequency of each id
        const idFrequency = {};
        nodes.forEach(node => {
            idFrequency[node.id] = (idFrequency[node.id] || 0) + 1;
        });


        // Sort the nodes based on id frequency
        nodes.sort((a, b) => idFrequency[a.id] - idFrequency[b.id]);

        // Parse ISO 8601 formatted time strings to create Date objects
        nodes.forEach(function (d) {
            d.time = new Date(d.time);
        });

        // Create the scales.
        const x = d3.scaleUtc()
            .domain(d3.extent(nodes, d => d.time))
            .rangeRound([marginLeft, width - marginRight]);

        const y = d3.scaleBand()
            .domain(nodes.map(d => d.id))
            .rangeRound([height - marginBottom, marginTop])
            .padding(1);

        // Adjust color scale based on eType
        const color = d3.scaleOrdinal()
            .domain(nodes.map(d => d.eType))
            .range(d3.schemeCategory10); // You can replace this with your custom color array

        const svg = d3.select("#chart").append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("width", width)
            .attr("height", height)
            .attr("style", "max-width: 100%; height: auto;");

        const tooltip = d3.select("#tooltip") // Select the tooltip by ID
            .append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        svg.append("g")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
            .call(g => g.select(".domain").remove());

        svg.append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove())
            .call(g => g.selectAll(".tick text").attr("dy", "0.35em")); // Adjust y-axis label position

        svg.append("g")
            .attr("stroke", "currentColor")
            .attr("stroke-opacity", 0.1)
            .call(g => g.append("g")
                .selectAll("line")
                .data(x.ticks())
                .join("line")
                .attr("x1", d => 0.5 + x(d))
                .attr("x2", d => 0.5 + x(d))
                .attr("y1", marginTop)
                .attr("y2", height - marginBottom))
            .call(g => g.append("g")
                .selectAll("line")
                .data(y.domain())
                .join("line")
                .attr("y1", d => 0.5 + y(d))
                .attr("y2", d => 0.5 + y(d))
                .attr("x1", marginLeft)
                .attr("x2", width - marginRight));

        function hideTooltip() {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        }

        d3.select(".Button").on("click", function () {
            // Reset the tooltip and selected node
            hideTooltip();
            selectedNode = null;
        });

        const typeLabel = ["Person", "Person", "Person", "Product", "Document", "Financial", "Country"];

        svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .join("circle")
            .attr("cx", d => x(d.time))
            .attr("cy", d => y(d.id) + y.bandwidth() / 2)
            .attr("r", 4) // Adjust the radius of the circles as needed
            .attr("fill", d => color(d.eType))
            .on("mouseover", function (event, d) {
                
                if (!tooltipVisible) { // Only show tooltip if it's not already visible
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                    tooltip.html("Node ID: " + d.id + "<br/>" + "Target ID: " + d.target + "<br/>" + "Type: " + typeLabel[d.eType] + "<br/>" + "Time: " + d.time)
                        .style("left", (event.pageX) + "px")
                        .style("top", (event.pageY - 28) + "px");
                }
                d3.select(this).style("fill", 'red');
            })
            .on("click", function (event, d) {
                if (selectedNode && selectedNode.id === d.id && +selectedNode.time === +d.time) {
                    // If the same node is clicked again, unselect it
                    d3.select(this).classed("selected", false);
                    selectedNode = null;
                    // Hide the tooltip
                    hideTooltip();
                } else {
                    // If a different node is clicked, unselect the previously selected node
                    svg.selectAll("circle").classed("selected", false);
                    // Apply the "selected" class only to the clicked circle
                    d3.select(this).classed("selected", true);
                    // Set the selected node ID and time
                    selectedNode = { id: d.id, time: d.time };
                    // Ensure tooltip remains visible when a node is clicked
                    tooltipVisible = true;
                    // Update the tooltip content
                    tooltip.html("Node ID: " + d.id + "<br/>" + "Target ID: " + d.target + "<br/>" + "Type: " + typeLabel[d.eType] + "<br/>" + "Time: " + d.time);
                    // Show the tooltip
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9)
                        .style("left", (event.pageX) + "px")
                        .style("top", (event.pageY - 28) + "px");
                }
            })
            .on("mouseout", function (d) {
                if (!tooltipVisible) { // Only hide tooltip if it's not supposed to remain visible
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                }
                d3.select(this).style("fill", d => color(d.eType));
            });


        // Create legend
        const legendContainer = d3.select("#legend-container");

        // Create legend inside the container
        const legend = legendContainer.append("svg")
            .attr("width", 100) // Set the width of the legend SVG
            .attr("height", 100) // Set the height of the legend SVG
            // You can add more attributes/styles as needed
            .append("g")

            .attr("font-family", "sans-serif")
            .attr("font-size", 10)
            .selectAll("g")
            .data(color.domain())
            .join("g")
            .attr("transform", (d, i) => `translate(0, ${i * 20})`);

        legend.append("rect")
            .attr("x", 0)
            .attr("width", 10)
            .attr("height", 10)
            .attr("fill", color);

        const colorLabels = ["Email", "Phone", "Sell", "Buy", "Co-authorship", "Financial", "Travels-to"];

        legend.append("text")
            .attr("x", 15)
            .attr("y", 5)
            .attr("dy", "0.35em")
            .text(d => {
                return colorLabels[d];
            });

    });
}
