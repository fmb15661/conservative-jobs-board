import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/jobs.json")
      .then((res) => res.json())
      .then((data) => setJobs(data))
      .catch((err) => console.error("Error loading jobs.json", err));
  }, []);

  const filteredJobs = jobs.filter((job) =>
    job.organization.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-center">
        Conservative Jobs Board
      </h1>

      <input
        type="text"
        placeholder="Search organizations..."
        className="w-full border rounded-lg p-2 mb-6"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {filteredJobs.length === 0 ? (
        <p className="text-center text-gray-500">
          No organizations match your search.
        </p>
      ) : (
        <ul className="space-y-4">
          {filteredJobs.map((job, idx) => (
            <li
              key={idx}
              className="p-4 border rounded-lg shadow hover:shadow-md transition"
            >
              <h2 className="text-xl font-semibold">{job.organization}</h2>
              <a
                href={job.career_page}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                View Careers
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
