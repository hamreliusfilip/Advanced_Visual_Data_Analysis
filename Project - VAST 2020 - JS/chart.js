function createChart(chartSelector, dataURL, width, height, centerPos) {
    var chargeStrength = -150; 
    var simulation; 

    d3.csv(dataURL).then(function (data) {
        var nodes = [];
        var links = [];
        var types = [];

        data.forEach(function (d) {
            var sourceNode = nodes.find(node => node.id === d.Source);
            var targetNode = nodes.find(node => node.id === d.Target);

            if (d.eType == 5) {
                return;
            }

            if (!sourceNode) {
                sourceNode = { id: d.Source };
                nodes.push(sourceNode);
            }

            if (!targetNode) {
                targetNode = { id: d.Target };
                nodes.push(targetNode);
            }

            links.push({ source: sourceNode, target: targetNode, type: d.eType });
            types.push(d.eType);
        });

        const color = d3.scaleOrdinal()
            .domain(types)
            .range(d3.schemeCategory10);

        simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(chargeStrength))
            .force("center", d3.forceCenter(centerPos[0], centerPos[1]))
            .on("tick", ticked);

        // Select and remove the existing SVG element
        d3.select(chartSelector).selectAll("svg").remove();

        // Append a new SVG element
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
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
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
            .attr("stroke", d => color(d.type))
            .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

        const node = svg.append("g")
            .attr("fill", "currentColor")
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
            .selectAll("g")
            .data(nodes)
            .join("g")
            .call(drag(simulation));

        node.append("circle")
            .attr("stroke", "black")
            .attr("stroke-width", 1.5)
            .attr("r", 5);

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

    legend.selectAll(".legend-text")
        .data(uniqueColors)
        .enter().append("text")
        .attr("class", "legend-text")
        .attr("x", legendBoxSize + 5)
        .attr("y", (d, i) => i * (legendBoxSize + 5) + legendBoxSize / 2)
        .attr("dy", "0.35em")
        .text(d => `${typeDescription[d]}`);

    simulation.on("tick", () => {
        link.attr("d", linkArc);
        node.attr("transform", d => `translate(${d.x},${d.y})`);
    });
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

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }
}
