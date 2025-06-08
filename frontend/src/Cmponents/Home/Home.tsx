import React from 'react';
import "./Home.scss"

function Home() {
  return (
    <div id="home-container">
      <h1>My Weekly Diary</h1>

      <div id="columns-container">
        <div id="first-column"> {/* Renamed to first-column */}
          <div className="input-group">
            <label htmlFor="entry-date">Date:</label>
            <input type="date" id="entry-date" />
          </div>

          <div className="input-group">
            <label htmlFor="effort-type">Effort Type:</label>
            <select id="effort-type">
              <option value="">Select Type</option>
              <option value="Deliverable">Deliverable</option>
              <option value="Learning">Learning</option>
              <option value="Process">Process</option>
            </select>
          </div>

          <div id="description-container" className="input-group">
            <label htmlFor="description-input">Description:</label>
            <textarea placeholder="Enter Description" id="description-input"></textarea>
          </div>

          <div className="input-group">
            <label htmlFor="genai-description">GenAI Description:</label>
            <textarea
              id="genai-description"
              placeholder="Generated AI Description will appear here"
              readOnly
            ></textarea>
          </div>
        </div> {/* End of first-column */}

        <div id="second-column"> {/* Renamed to second-column */}
          <div className="input-group">
            <label htmlFor="links">Links:</label>
            <input type="text" id="links" placeholder="Add relevant links (e.g., Jira, Confluence)" />
          </div>

          <div className="input-group">
            <label htmlFor="status">Status:</label>
            <select id="status">
              <option value="">Select Status</option>
              <option value="Not Started">Not Started</option>
              <option value="In Progress">In Progress</option>
              <option value="Completed">Completed</option>
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="impact-outcome">Impact/Outcome:</label>
            <select id="impact-outcome">
              <option value="">Select Impact/Outcome</option>
              <option value="Knowledge Sharing">Knowledge Sharing</option>
              <option value="Process Improvement">Process Improvement</option>
              <option value="Process Change">Process Change</option>
              <option value="Process Learning">Process Learning</option>
              <option value="Associate Learning">Associate Learning</option>
              <option value="Improved Testing">Improved Testing</option>
              <option value="Product Enhancement">Product Enhancement</option>
              <option value="New Feature">New Feature</option>
              <option value="Bug Fix">Bug Fix</option>
              <option value="CI/CD">CI/CD</option>
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="additional-notes">Additional Notes:</label>
            <textarea id="additional-notes" placeholder="Any other relevant notes"></textarea>
          </div>
        </div> {/* End of second-column */}
      </div>
    </div>
  );
}

export default Home;