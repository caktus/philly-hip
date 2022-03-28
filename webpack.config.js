const webpack = require('webpack');
const path = require('path');

module.exports = {
    bail: true,
    mode: 'none',
    context: __dirname,
    entry: ['./hip/static/js/webpack_entry.js'],
    resolve: {
        extensions: ['*', '.js'],
    },
    output: {
        path: path.resolve('./hip/static/js/bundles/'),
        filename: '[name].js',
    },
    module: {
        rules: [
            {
                test: /\.(js)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
    ]
};