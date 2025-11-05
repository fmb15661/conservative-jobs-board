import { useEffect, useState } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function load() {
      const r = await fetch("/jobs.json");
      const data = await r.json();
      setJobs(data);
    }
    load();
  }, []);

  const filtered = jobs.filter((j) =>
    (j.title + " " + j.organization + " " + j.location)
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "20px", fontFamily: "Arial" }}>
      <h1 style={{ textAlign: "center", marginBottom: "30px" }}>Conservative Jobs Board</h1>

      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search jobs..."
        style={{
          width: "100%",
          padding: "14px",
          marginBottom: "30px",
          fontSize: "18px",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
      />

      {filtered.map((j, i) => (
        <div
          key={i}
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "16px",
            marginBottom: "20px",
            background: "#fff",
          }}
        >
          <h2 style={{ margin: "0 0 8px" }}>{j.title}</h2>
          <p style={{ margin: "0 0 4px" }}><strong>{j.organization}</strong></p>
          <p style={{ margin: "0 0 4px" }}>{j.location}</p>
          <p style={{ margin: "0 0 8px", color: "#777" }}>{j.date_posted}</p>
          <a href={j.link} target="_blank" style={{ color: "#0066CC" }}>
            View Job
          </a>
        </div>
      ))}
    </div>
  );
}

