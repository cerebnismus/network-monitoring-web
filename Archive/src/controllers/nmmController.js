import mongoose from 'mongoose';
import { ContactSchema } from '../models/nmmModel';
import { NodeSchema } from '../models/nmmModel';
import { DataSchema } from '../models/nmmModel';


// CONTACT CONTROLLER
const Contact = mongoose.model('Contact', ContactSchema);
export const addNewContact = (req,res) => {
	let newContact = new Contact(req.body);

	newContact.save((err, contact) => {
		if (err) {
			res.send(err);
		}
		res.json(contact);
	});
}
export const getContacts = (req,res) => {
	Contact.find({}, (err, contact) => {
		if (err) {
			res.send(err);
		}
		res.json(contact);
	});
}
export const getContactWithID = (req,res) => {
	Contact.findById(req.params.contactID, (err, contact) => {
		if (err) {
			res.send(err);
		}
		res.json(contact);
	});

}
export const updateContact = (req,res) => {
	Contact.findOneAndUpdate({ _id: req.params.contactID }, req.body, { new: true, useFindAndModify: false }, (err, contact) => {
		if (err) {
			res.send(err);
		}
		res.json(contact);
	});

}
export const deleteContact = (req,res) => {
	Contact.remove({ _id: req.params.contactID }, (err, contact) => {
		if (err) {
			res.send(err);
		}
		res.json({ message: 'succesfully deleted contact'});
	});
}

// NODE CONTROLLER
const Node = mongoose.model('Node', NodeSchema);
export const addNewNode = (req,res) => {
	let newNode = new Node(req.body);

	newNode.save((err, node) => {
		if (err) {
			res.send(err);
		}
		res.json(node);
	});
}
export const getNodes = (req,res) => {
	Node.find({}, (err, node) => {
		if (err) {
			res.send(err);
		}
		res.json(node);
	});
}
export const getNodeWithID = (req,res) => {
	Node.findById(req.params.nodeID, (err, node) => {
		if (err) {
			res.send(err);
		}
		res.json(node);
	});

}
export const updateNode = (req,res) => {
	Node.findOneAndUpdate({ _id: req.params.nodeID }, req.body, { new: true, useFindAndModify: false }, (err, node) => {
		if (err) {
			res.send(err);
		}
		res.json(node);
	});

}
export const deleteNode = (req,res) => {
	Node.remove({ _id: req.params.nodeID }, (err, node) => {
		if (err) {
			res.send(err);
		}
		res.json({ message: 'succesfully deleted node'});
	});
}

// DATA CONTROLLER
const Data = mongoose.model("Data", DataSchema);
export const addNewData = (req,res) => {
	// create a new node
	let newData = new Data(req.body);
	let ipData = newData.ipaddress;
	let statusData = newData.status;
	let idData = newData._id;
	const { exec } = require("child_process");
	exec(`ping -c 1 ${ipData} &> /dev/null && echo 'UP' || echo 'DOWN' | head -n1`, (error, stdout, stderr) => {
		if (error) {
			console.log(`error: ${error.message}`);
			return;
		}
		if (stderr) {
			console.log(`stderr: ${stderr}`);
			return;
		}
		console.log(`Controller ping status raw: ${stdout}`);
		newData.save((err, data) => {
			if (err) {
				res.send(err);
			}
			Data.findOneAndUpdate({ _id: idData }, {$set: {status: stdout}}, {upsert: true, useFindAndModify: false }, (err, data) => {
				console.log(`2: ${stdout}`);
				console.log(`2: ${statusData}`);
				console.log(`2: ${data.status}`);
				res.json(data);
			});
		});

	});
}