function toggleEdgesVisibility(chartSelector, edgeTyp) {
    console.log("Toggling edges of type:", edgeType);

    const svg = d3.select(chartSelector).select("svg");

    const edges = svg.selectAll("path");

    edges.each(function (d) {
        console.log("Edge data:", d); // Log the data associated with each edge
        // Convert d.type to a number for comparison
        const edgeTypeNumber = parseInt(d.type);
        if (edgeTypeNumber === edgeType) {
            console.log("Edge type matched. Current visibility:", d3.select(this).style("display")); // Log the current visibility
            const isVisible = d3.select(this).style("display") !== "none";
            d3.select(this).style("display", isVisible ? "none" : null);
            console.log("Updated visibility:", d3.select(this).style("display")); // Log the updated visibility
        }
    });
}

function createChart(chartSelector, dataURL, width, height, centerPos, selectedEdgeType) {

    var chargeStrength = -150;
    var simulation;

    function updateChargeStrength(chargeStrength) {
        simulation.force('charge', d3.forceManyBody().strength(chargeStrength));
        simulation.alpha(0.3).restart();
    }

    d3.select('#chargeSlider').on('input', function () {
        chargeStrength = +this.value;
        d3.select('#chargeValue').text(chargeStrength);
        updateChargeStrength(chargeStrength);
    });

    d3.csv(dataURL).then(function (data) {

        var nodes = [];
        var links = [];
        var types = [];

        data.forEach(function (d) {
            var sourceNode = nodes.find(node => node.id === d.Source);
            var targetNode = nodes.find(node => node.id === d.Target);

            if(d.eType == 5){
                return;
            }

            if(selectedEdgeType != 10){ 
                if (d.eType != selectedEdgeType) {
                    return;
                }
            }
           
            if (!sourceNode) {
                sourceNode = { id: d.Source, eType: d.eType };
                nodes.push(sourceNode);
            }

            if (!targetNode) {
                targetNode = { id: d.Target, eType: d.eType };
                nodes.push(targetNode);
            }

            links.push({ source: sourceNode, target: targetNode, type: d.eType });
            types.push(d.eType);
        });

        nodes.sort((a, b) => a.eType - b.eType);

        const color = d3.scaleOrdinal()
            .domain(types)
            .range(d3.schemeCategory10);

        simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(chargeStrength))
            .force("center", d3.forceCenter(centerPos[0], centerPos[1]))
            .on("tick", ticked);

        d3.select(chartSelector).selectAll("svg").remove();

        var svg = d3.select(chartSelector)
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        svg.append("defs").selectAll("marker")
            .data(types)
            .join("marker")
            .attr("id", d => `arrow-${d}`)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -0.5)
            .attr("markerWidth", 10)
            .attr("markerHeight", 10)
            .attr("orient", "auto")
            .append("path")
            .attr("fill", color)
            .attr("d", "M0,-5L10,0L0,5");

        const link = svg.append("g")
            .attr("fill", "none")
            .attr("stroke-width", 1.5)
            .selectAll("path")
            .data(links)
            .join("path")
            .attr("stroke", "grey")
            .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`)
            .attr("fill", "none");

        const node = svg.append("g")
            .attr("fill", "currentColor")
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
            .selectAll("g")
            .data(nodes)
            .join("g")
            .call(drag(simulation));

        const symbolType = d3.scaleOrdinal()
            .domain([0, 1, 2, 3, 4, 5, 6])
            .range([d3.symbolCircle, d3.symbolCircle, d3.symbolCircle, d3.symbolCross, d3.symbolSquare, d3.symbolTriangle, d3.symbolStar]);

        node.append("path")
            .attr("d", d => d3.symbol().type(symbolType(d.eType))());

        node.append("text")
            .attr("x", 8)
            .attr("y", "0.31em")
            .text(d => d.id)
            .clone(true).lower()
            .attr("fill", "black")
            .attr("font-weight", "bold");

        const legend = svg.append("g")
            .attr("class", "legend")
            .attr("transform", "translate(20,20)");

        const uniqueColors = Array.from(new Set(types)).sort((a, b) => a - b);
        const legendBoxSize = 15;

        legend.selectAll(".legend-box")
            .data(uniqueColors)
            .enter().append("rect")
            .attr("class", "legend-box")
            .attr("x", 0)
            .attr("y", (d, i) => i * (legendBoxSize + 5))
            .attr("width", legendBoxSize)
            .attr("height", legendBoxSize)
            .style("fill", color);

        const typeDescription = ["Email (Communication)", "Phone (Communication)", "Sell (Procurement)", "Buy (Procurement)", "Co-authorship channel", "Demographics channel (Income/expenses)", "Travel channel"];
        const symbolDescription = ["Person", "Person", "Person", "Product", "Document", "Country", "Travel channel"];

        legend.selectAll(".legend-text")
            .data(uniqueColors)
            .enter().append("text")
            .attr("class", "legend-text")
            .attr("x", legendBoxSize + 5)
            .attr("y", (d, i) => i * (legendBoxSize + 5) + legendBoxSize / 2)
            .attr("dy", "0.35em")
            .text(d => `${typeDescription[d]}`);

        const symbolLegend = svg.append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${width - 150}, 20)`); // Adjust x and y coordinates here

        symbolLegend.selectAll(".legend-symbol")
            .data(uniqueColors)
            .enter().append("g")
            .attr("class", "legend-symbol")
            .attr("transform", (d, i) => `translate(0, ${i * 25})`) // Adjust the spacing between symbols
            .each(function (d) {
                d3.select(this).append("path")
                    .attr("d", d3.symbol().type(symbolType(d))())
                    .attr("stroke", "black")
                    .attr("stroke-width", 1.5);
            });

        symbolLegend.selectAll(".legend-text")
            .data(uniqueColors)
            .enter().append("text")
            .attr("class", "legend-text")
            .attr("x", 20) // Adjust the x position of text
            .attr("y", (d, i) => i * 25) // Adjust the y position of text
            .attr("dy", "0.35em")
            .text(d => `${symbolDescription[d]}`);

        simulation.on("tick", () => {
            link.attr("d", linkArc);
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });

        function ticked() {
            link.attr("d", linkArc);
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        }
    });

    function linkArc(d) {
        const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
        return `
          M${d.source.x},${d.source.y}
          A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
        `;
    }

    function drag(simulation) {
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        function getShape(d) {
            let shape;

            if (d === 1 || d === 2) {
                shape = d3.symbol(d3.symbolCircle);
            } else if (d === 3) {
                shape = d3.symbol(d3.symbolCross);
            } else if (d === 4) {
                shape = d3.symbol(d3.symbolSquare);
            } else if (d === 5) {
                shape = d3.symbol(d3.symbolTriangle);
            } else if (d === 6) {
                shape = d3.symbol(d3.symbolStar);
            }
            return shape;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }
}

function getSelectedFilePath() {

    var selectedValue = document.getElementById("seeds").value;

    if (selectedValue === "Seed 1 - 1 level") {
        return 'Seed_Structure_data/output_total_seedOne.csv';

    } else if (selectedValue === "Seed 2 - 1 level") {
        return 'Seed_Structure_data/output_total_seedTwo.csv';

    } else if (selectedValue === "Seed 3 - 1 level") {
        return 'Seed_Structure_data/output_total_seedThree.csv';
    } else if (selectedValue === "Seed 1 - 2 level co_aut") {
        return 'Seed_Structure_data/SeedOne_2Levels_FilteredOn_FrequentEdges.csv';
    }
    else if (selectedValue === "SeedThree_Buyers") {
        return 'Seed_Structure_data/seedThreeBuyerTimeCONTROLTEST.csv';
    }
    
}