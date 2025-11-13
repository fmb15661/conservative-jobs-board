import { useEffect, useState } from "react";

const TYPE_MAP = {
  ops: "Operations",
  comms: "Communications",
  legal: "Legal",
  policy: "Policy",
  media: "Media",
  ga: "Government Affairs",
  intern: "Internship",
  dev: "Development",
};

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function go() {
      const r = await fetch("/jobs.json");
      const data = await r.json();
      setJobs(data);
    }
    go();
  }, []);

  const filtered = jobs.filter((j) =>
    (j.title + j.organization + j.location + (TYPE_MAP[j.type] || ""))
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-6">
          Conservative Jobs Board
        </h1>

        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search jobs..."
          className="w-full p-2 border border-gray-300 rounded-lg mb-6"
        />

        <div className="overflow-x-auto">
          <table className="table w-full border-collapse">
            <thead>
              <tr className="bg-white">
                <th className="text-left p-2 border border-gray-300">Title</th>
                <th className="text-left p-2 border border-gray-300">Organization</th>
                <th className="text-left p-2 border border-gray-300">Location</th>
                <th className="text-left p-2 border border-gray-300">Date Posted</th>
                <th className="text-left p-2 border border-gray-300">Job Type</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((j, i) => (
                <tr key={i} className="bg-white hover:bg-gray-50">
                  <td className="p-2 border border-gray-300">
                    <a href={j.link} target="_blank" className="text-blue-600 hover:underline">
                      {j.title}
                    </a>
                  </td>
                  <td className="p-2 border border-gray-300">{j.organization}</td>
                  <td className="p-2 border border-gray-300">{j.location}</td>
                  <td className="p-2 border border-gray-300">{j.date_posted}</td>
                  <td className="p-2 border border-gray-300">{TYPE_MAP[j.type] || ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
