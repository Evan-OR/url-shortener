//Check if link already exists
//takes created connection from index.js
const checkIfLinkExists = async (connection, url, callback) => {
  const sql = 'SELECT * FROM urls_info where original_url = ?;';
  connection.query(sql, [url], (err, rows, tables) => {
    if (err) {
      return console.log(err);
    }

    callback(err, rows[0]);
  });
};

module.exports = {
  checkIfLinkExists,
};
