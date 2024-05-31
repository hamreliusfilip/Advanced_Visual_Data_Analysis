function createAxisChart(dataURL) {

    function convertTimestamp(timestamp) {
        var milliseconds = timestamp * 1000;

        var date = new Date(2025, 0, 1); 
        date.setTime(date.getTime() - milliseconds);

        return date.toISOString();
    }

    d3.csv(dataURL).then(function (data) {
        var nodes = [];

        data.forEach(function (d) {
            if (d.eType != 5) {
                if (d.Time >= 0) { 
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

        const idFrequency = {};
        nodes.forEach(node => {
            idFrequency[node.id] = (idFrequency[node.id] || 0) + 1;
        });

        nodes.sort((a, b) => idFrequency[a.id] - idFrequency[b.id]);


        nodes.forEach(function (d) {
            d.time = new Date(d.time);
        });


        const x = d3.scaleUtc()
            .domain(d3.extent(nodes, d => d.time))
            .rangeRound([marginLeft, width - marginRight]);

        const y = d3.scaleBand()
            .domain(nodes.map(d => d.id))
            .rangeRound([height - marginBottom, marginTop])
            .padding(1);

        const color = d3.scaleOrdinal()
            .domain(nodes.map(d => d.eType))
            .range(d3.schemeCategory10); 

        const svg = d3.select("#chart").append("svg")
            .attr("viewBox", [0, 0, width, height])
            .attr("width", width)
            .attr("height", height)
            .attr("style", "max-width: 100%; height: auto;");

        const tooltip = d3.select("#tooltip") 
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
            .call(g => g.selectAll(".tick text").attr("dy", "0.35em")); 

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
            .attr("r", 4) 
            .attr("fill", d => color(d.eType))
            .on("mouseover", function (event, d) {
                
                if (!tooltipVisible) { 
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
                    d3.select(this).classed("selected", false);
                    selectedNode = null;
                    hideTooltip();
                } else {
                   
                    svg.selectAll("circle").classed("selected", false);
              
                    d3.select(this).classed("selected", true);
                  
                    selectedNode = { id: d.id, time: d.time };
              
                    tooltipVisible = true;
                  
                    tooltip.html("Node ID: " + d.id + "<br/>" + "Target ID: " + d.target + "<br/>" + "Type: " + typeLabel[d.eType] + "<br/>" + "Time: " + d.time);
                 
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9)
                        .style("left", (event.pageX) + "px")
                        .style("top", (event.pageY - 28) + "px");
                }
            })
            .on("mouseout", function (d) {
                if (!tooltipVisible) { 
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                }
                d3.select(this).style("fill", d => color(d.eType));
            });


 
        const legendContainer = d3.select("#legend-container");

       
        const legend = legendContainer.append("svg")
            .attr("width", 100) 
            .attr("height", 100) 
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
