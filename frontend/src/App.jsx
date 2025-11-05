import { useEffect, useState } from "react";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function go() {
      const r1 = await fetch("/jobs_talentmarket.json");
      const tm = await r1.json();

      const r2 = await fetch("/jobs_yaf.json");
      const yaf = await r2.json();

      // combine both sources
      setJobs([...tm, ...yaf]);
    }
    go();
  }, []);

  const filtered = jobs.filter((j) =>
    (j.title + j.organization + j.location)
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Conservative Jobs Board</h1>

      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search jobs..."
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "20px",
          fontSize: "16px",
        }}
      />

      {filtered.map((j, i) => (
        <div
          key={i}
          style={{
            border: "1px solid #ccc",
            margin: "10px 0",
            padding: "10px",
          }}
        >
          <h3>{j.title}</h3>
          <p>
            <strong>{j.organization}</strong>
          </p>
          <p>{j.location}</p>
          <p>{j.date_posted}</p>
          <a href={j.link} target="_blank">
            View Job
          </a>
        </div>
      ))}
    </div>
  );
}

