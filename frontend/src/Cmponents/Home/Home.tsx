import React, { useState } from 'react';
import "./Home.scss"
import { EFFORT_TYPE, IMPACT, STATUS } from '../../utills/DiaryInput.ts';

function Home() {
  const [isGenAIEnabled, setIsGenAIEnabled] = useState(false);
  const [date, setDate] = useState('');
  const [effortType, setEffortType] = useState('');
  const [description, setDescription] = useState('');
  const [links, setLinks] = useState('');
  const [status, setStatus] = useState(STATUS[0]);
  const [impact, setImpact] = useState(IMPACT[0]);
  const [additionalNotes, setAdditionalNotes] = useState('');

  const generateAIDescription = () => {
    setIsGenAIEnabled(true);
  };

  return (
    <div id="home-container">
      <h1>My Weekly Diary</h1>

      <div id="columns-container">
        <div id="first-column"> 
          <div className="input-group">
            <label htmlFor="entry-date">Date:</label>
            <input
              type="date"
              id="entry-date"
              value={date}
              onChange={e => setDate(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label htmlFor="effort-type">Effort Type:</label>
            <select
              id="effort-type"
              value={effortType}
              onChange={e => setEffortType(e.target.value)}
            >
              <option value="">Select Type</option>
              {EFFORT_TYPE.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div id="description-container" className="input-group">
            <label htmlFor="description-input">Description:</label>
            <textarea
              placeholder="Enter Description"
              id="description-input"
              value={description}
              onChange={e => setDescription(e.target.value)}
            ></textarea>
          </div>

          {isGenAIEnabled ? (
            <div className="input-group">
              <label htmlFor="genai-description">GenAI Description:</label>
              <textarea
                id="genai-description"
                placeholder="Generated AI Description will appear here"
                readOnly
              ></textarea>
            </div>
          ) : (
            <button
              onClick={generateAIDescription}
              id="genai-button" className='btn'>
              Generate GenAI Description
              <span className="icon">🤖</span>
            </button>

          )}

        </div> 


        <div id="second-column">
          <div className="input-group">
            <label htmlFor="links">Links:</label>
            <input
              type="text"
              id="links"
              placeholder="Add relevant links (e.g., Jira, Confluence)"
              value={links}
              onChange={e => setLinks(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label htmlFor="status">Status:</label>
            <select
              id="status"
              value={status}
              onChange={e => setStatus(e.target.value)}
            >
              {STATUS.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="impact-outcome">Impact/Outcome:</label>
            <select
              id="impact-outcome"
              value={impact}
              onChange={e => setImpact(e.target.value)}
            >
              {IMPACT.map((impact) => (
                <option key={impact} value={impact}>
                  {impact}
                </option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="additional-notes">Additional Notes:</label>
            <textarea
              id="additional-notes"
              placeholder="Any other relevant notes"
              value={additionalNotes}
              onChange={e => setAdditionalNotes(e.target.value)}
            ></textarea>
          </div>
        </div> 
      </div>
    </div>
  );
}

export default Home;