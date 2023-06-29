const path = require("path");
const webpack = require("webpack");

module.exports = (env, argv) => {
	return {
		entry: "./src/index.js",
		output: {
			path: path.resolve(__dirname, "./static/frontend"),
			filename: "[name].js",
		},
		module: {
			rules: [
				{
					test: /\.js$/,
					exclude: /node_modules/,
					use: {
						loader: "babel-loader",
						options: {
							presets: ["@babel/preset-env", "@babel/preset-react"],
						},
					},
				},
				{
					test: /\.jsx$/,
					use: {
						loader: "babel-loader",
						options: {
							presets: ["@babel/preset-env", "@babel/preset-react"],
						},
					},
				},
			],
		},
		optimization: {
			minimize: true,
		},
		plugins: [
			new webpack.DefinePlugin({
				"process.env": {
					NODE_ENV: JSON.stringify(argv.mode),
				},
			}),
		],
	};
};
