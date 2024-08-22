import React from "react";
import { useState } from "react";

export default function App() {
	const [data, setData] = useState("Blank");

	function getFoo() {
		fetch("/api/Foo", {
			method: "GET",
		})
			.then((response) => {
				if (response.ok) {
					return response.json();
				} else {
					throw new Error("Error: " + response.status);
				}
			})
			.then((data) => {
				setData(data.word);
			});
	}
	return (
		<>
			Hello React!
			<br />
			<button onClick={getFoo}>Data {data}</button>
		</>
	);
}
