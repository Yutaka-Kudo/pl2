

Vue.component('bar_sales', {
    extends: VueChartJs.Bar,
    props: ["data", "options"],
    mounted() {
        this.addPlugin(dataLabelPluginForBar,);
        this.renderChart(this.data, this.options);
    }
})


Vue.component('pie_costs', {
    extends: VueChartJs.Pie,
    name: 'pie_costs',
    props: ["data", "options"],
    mounted() {
        this.addPlugin(dataLabelPlugin,);
        this.renderChart(this.data, this.options);
    },
})

Vue.component('bar_costs', {
    extends: VueChartJs.Bar,
    name: 'bat_costs',
    props: ["data", "options"],
    mounted() {
        this.addPlugin(dataLabelPluginForBar,);
        this.renderChart(this.data, this.options);
    },
})


// Define a plugin to provide data labels
// Chart.plugins.register({ //全体に利かす
var dataLabelPlugin = { //個別に利かす
    afterDatasetsDraw: function (chart, easing) {
        // To only draw at the end of animation, check for easing === 1
        var ctx = chart.ctx;

        chart.data.datasets.forEach(function (dataset, i) {

            // //割合を求めるため、合計値を出すーーーーー
            // var dataSum = 0;
            // dataset.data.forEach(function (element) {
            //     dataSum += element;
            // });

            var meta = chart.getDatasetMeta(i);
            if (!meta.hidden) {
                meta.data.forEach(function (element, index) {
                    // Draw the text in black, with the specified font
                    ctx.fillStyle = 'rgb(0, 0, 0)';

                    var fontSize = 11;
                    var fontStyle = 'normal';
                    var fontFamily = 'Helvetica Neue';
                    ctx.font = Chart.helpers.fontString(fontSize, fontStyle, fontFamily);

                    // Just naively convert to string for now
                    var labelString = chart.data.labels[index].toString();
                    var dataString = dataset.data[index].toLocaleString();
                    // var percentageString = (Math.round(dataset.data[index] / dataSum * 1000) / 10).toString() + "%"; //割合を求める

                    // Make sure alignment settings are correct
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';

                    var padding = 5;
                    var position = element.tooltipPosition();
                    ctx.fillText(labelString, position.x, position.y - (fontSize / 2) - padding);
                    ctx.fillText(dataString, position.x, position.y + (fontSize / 2) - padding);
                    // ctx.fillText(percentageString, position.x, position.y + (fontSize * 1.5) - padding);
                });
            }
        });
    }
    // });
};

var dataLabelPluginForBar = { //個別に利かす
    afterDatasetsDraw: function (chart, easing) {
        // To only draw at the end of animation, check for easing === 1
        var ctx = chart.ctx;

        chart.data.datasets.forEach(function (dataset, i) {

            // //割合を求めるため、合計値を出すーーーーー
            // var dataSum = 0;
            // dataset.data.forEach(function (element) {
            //     dataSum += element;
            // });

            var meta = chart.getDatasetMeta(i);
            if (!meta.hidden) {
                meta.data.forEach(function (element, index) {
                    // Draw the text in black, with the specified font
                    ctx.fillStyle = 'rgb(0, 0, 0)';

                    var fontSize = 15;
                    var fontStyle = 'normal';
                    var fontFamily = 'Helvetica Neue';
                    ctx.font = Chart.helpers.fontString(fontSize, fontStyle, fontFamily);

                    // Just naively convert to string for now
                    var dataString = dataset.data[index].toLocaleString();
                    // var percentageString = (Math.round(dataset.data[index] / dataSum * 1000) / 10).toString() + "%"; //割合を求める

                    // Make sure alignment settings are correct
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';

                    var padding = 5;
                    var position = element.tooltipPosition();
                    ctx.fillText(dataString, position.x, position.y + (fontSize *1.5) - padding);
                    // ctx.fillText(percentageString, position.x, position.y + (fontSize * 1.5) - padding);
                });
            }
        });
    }
    // });
};