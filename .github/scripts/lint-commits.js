"use strict";

const { URL } = require("url");

const titleRegex = /^(.+?)(?:(?:\r?\n){2}|$)/us;
const titleOf = (message) => message.match(titleRegex)[1];
const bodyOf = (message) => message.slice(titleOf(message).length).trimStart();

const urlRegex = /^(?:https?|ftp):\/\//u;
function isURL(string) {
  if (urlRegex.test(string)) {
    try {
      new URL(string);
      return true;
    } catch {}
  }

  return false;
}

const checkers = [{
  error: "Commit message must not contain carriage return (\\r) characters",
  check: (message) => !message.includes("\r"),
}, {
  error: "Commit title must not contain newline (\\n) characters",
  check: (message) => !titleOf(message).includes("\n"),
}, {
  error: "Commit title must be 50 characters long or less",
  check: (message) => titleOf(message).length <= 50,
}, {
  error: "Commit title must start with an uppercase letter",
  check(message) {
    const firstChar = titleOf(message).charAt(0);
    const firstCharUpper = firstChar.toUpperCase();
    return firstChar === firstCharUpper
      && "A" <= firstCharUpper
      && firstCharUpper <= "Z";
  },
}, {
  error: "Commit title must not end with a period",
  check: (message) => titleOf(message).trimEnd().slice(-1) !== ".",
}, {
  error: "Commit body lines must be 72 characters long or less (except URLs)",
  check(message) {
    const body = bodyOf(message);
    if (body.trimEnd() !== "") {
      for (const line of body.split("\n")) {
        if (line.length > 72 && !isURL(line)) {
          return false;
        }
      }
    }

    return true;
  },
}];

function runChecker({ check, error }) {
  return check(this.message) ? [] : [error];
}

function checkCommits(commits) {
  let success = true;
  for (const { commit, sha } of commits) {
    const errors = checkers.flatMap(runChecker, commit);
    if (errors.length === 0) {
      continue;
    }

    if (!success) {
      console.log("");
    }
    success = false;

    console.log("Commit %s failed these checks:", sha);
    for (const error of errors) {
      console.log("  %s", error);
    }
  }

  return success;
}

async function main(github, core, context) {
  const { repository, pull_request } = context.payload;
  const options = github.rest.pulls.listCommits.endpoint.merge({
    owner: repository.owner.login,
    repo: repository.name,
    pull_number: pull_request.number,
  });
  const commits = await github.paginate(options);
  const isErrorFree = checkCommits(commits);
  if (!isErrorFree) {
    core.setFailed("Please check the logs for errors in commit messages.");
  }
}

module.exports = { main };
