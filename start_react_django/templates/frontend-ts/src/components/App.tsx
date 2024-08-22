import React, { useState } from "react";

interface IData {
	text: string;
	color: string;
}

export default function App() {
	const [data, setData] = useState<IData>({ text: "Hello...", color: "#ffffff" });

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
				setData(data as IData);
			});
	}
	return (
		<>
			<div style={{ padding: "20px", display: "flex", flexDirection: "column", alignItems: "center", gap: "16px" }}>
				<div style={{ fontSize: "36px", color: data.color, transition: "100ms linear" }}>{data.text}</div>
				<button style={{ minWidth: "120px", fontSize: "24px" }} onClick={getFoo}>
					Get Foo!
				</button>
				<div style={{ fontSize: "12px", color: data.color, transition: "100ms linear" }}>
					Made with create-react-django by Joel Cutler
				</div>
			</div>
		</>
	);
}
