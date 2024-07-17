import { addNewContact,
		getContacts,
		getContactWithID,
		updateContact,
		deleteContact,
		addNewNode,
		getNodes,
		getNodeWithID,
		updateNode,
		deleteNode,
		addNewData,
} from '../controllers/nmmController';

const routes = (app) => {

	// CONTACT ROUTE
	app.route('/contact')
		.get((req, res, next) => {
			//middleware
			console.log(`Request from: ${req.originalUrl}`)
			console.log(`Request type: ${req.method}`)
			next();
		}, getContacts)

		// Post endpoint
		.post(addNewContact);

	app.route('/contact/:contactID')
		
		// get a specific contact
		.get(getContactWithID)

		// updating a specific contact
		.put(updateContact)

		// deleting a specific contact
		.delete(deleteContact);

	// NODES ROUTE
	app.route('/node')
		.get((req, res, next) => {
			//middleware
			console.log(`Request from: ${req.originalUrl}`)
			console.log(`Request type: ${req.method}`)
			next();
		}, getNodes)

		// Post endpoint
		.post(addNewNode);

	app.route('/node/:nodeID')
		
		// get a specific Node
		.get(getNodeWithID)

		// updating a specific Node
		.put(updateNode)

		// deleting a specific Node
		.delete(deleteNode);

	// DATA ROUTE
	app.route('/data')
		.post((req, res, next) => {
			// good middleware
			console.log(`Routes Request from: ${req.originalUrl}`)
			console.log(`Routes Request type: ${req.method}`)
			console.log(`Routes Request ep: ${req.body.nodename}`)		
			console.log(`Routes Request ip: ${req.body.ipaddress}`)		
			// calls next because it hasn't modified the header
			next();
		}, addNewData)

};

export default routes;