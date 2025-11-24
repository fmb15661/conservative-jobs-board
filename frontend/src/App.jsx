import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  const SOURCES = [
    "/jobs_talentmarket.json",
    "/jobs_yaf.json",
    "/jobs_afpi.json",
    "/jobs_hudson.json",
    "/jobs_cato.json",
    "/jobs_plf.json",
    "/jobs_ntu.json",
    "/jobs_acton.json",
    "/jobs_aier.json",
    "/jobs_excelined.json",
    "/jobs_claremont.json",
    "/jobs_heritage.json",
    "/jobs_cei.json",
    "/jobs_tppf.json",
    "/jobs_leadership_institute.json",
    "/jobs_crc.json",
    "/jobs_alec.json",
    "/jobs_acc.json",
    "/jobs_amprinproj.json",
    "/jobs_ashbrook.json",
    "/jobs_bri.json",
    "/jobs_commonwealth.json",
    "/jobs_fee.json",            //  <——— FEE IS NOW HERE
    "/jobs_fair_manual.json"     // FAIR manual
  ];

  const normalizeOrg = (org) => {
    if (!org) return "N/A";
    return org.replace(/–/g, "-").replace(/—/g, "-").trim();
  };

  const normalizeLocation = (loc) => {
    if (!loc) return "";
    return loc.replace(/\s+/g, " ").replace(/–/g, "-").replace(/—/g, "-").trim();
  };

  useEffect(() => {
    async function loadJobs() {
      let all = [];

      for (const src of SOURCES) {
        try {
          const res = await fetch(src);
          if (!res.ok) continue;

          const data = await res.json();
          const normalized = data.map((job) => ({
            title: job.title || "N/A",
            organization: normalizeOrg(job.organization),
            location: normalizeLocation(job.location),
            url: job.url || job.link || "",
          }));

          all = [...all, ...normalized];
        } catch (e) {
          console.error("Error fetching", src, e);
        }
      }

      // === CATO FIXES ===
      all = all.map((job) => {
        if (job.organization === "Cato Institute" && job.title.includes("Comic Artists")) {
          return { ...job, location: "Remote" };
        }
        if (job.organization === "Cato Institute" && job.location === "Cato Institute - Headquarters") {
          return { ...job, location: "Hybrid/Washington, D.C." };
        }
        if (job.organization === "Cato Institute" && job.location === "Hybrid - Cato Institute Headquarters") {
          return { ...job, location: "Hybrid/Washington, D.C." };
        }
        return job;
      });

      // === Commonwealth FIX ===
      all = all.map((job) => {
        if (
          job.organization === "Commonwealth Foundation" &&
          (
            job.title === "Director, Executive Office of the CEO" ||
            job.title === "Executive Assistant to the Chief Operating Officer and General Counsel"
          )
        ) {
          return { ...job, location: "Hybrid/Harrisburg, PA" };
        }
        return job;
      });

      setJobs(all);
    }

    loadJobs();
  }, []);

  const sortJobs = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  const sortedJobs = [...jobs].sort((a, b) => {
    if (!sortConfig.key) return 0;

    const aVal = a[sortConfig.key] || "";
    const bVal = b[sortConfig.key] || "";

    if (aVal < bVal) return sortConfig.direction === "asc" ? -1 : 1;
    if (aVal > bVal) return sortConfig.direction === "asc" ? 1 : -1;
    return 0;
  });

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold mb-6">Conservative Jobs Board</h1>

      <div className="grid grid-cols-4 gap-4 font-bold border-b pb-2 mb-2">
        <button onClick={() => sortJobs("title")}>Job Title</button>
        <button onClick={() => sortJobs("organization")}>Organization</button>
        <button onClick={() => sortJobs("location")}>Location</button>
        <span>Apply</span>
      </div>

      {sortedJobs.map((job, idx) => (
        <div key={idx} className="grid grid-cols-4 gap-4 border-b py-2">
          <div>{job.title}</div>
          <div>{job.organization}</div>
          <div>{job.location}</div>
          <div>
            {job.url ? (
              <a
                href={job.url}
                className="text-blue-600 underline"
                target="_blank"
                rel="noreferrer"
              >
                Apply
              </a>
            ) : (
              ""
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default App;

