import mongoose from 'mongoose';
const Schema = mongoose.Schema;

export const ContactSchema = new Schema({
	username: {type: String},
	email: {type: String},
	password: {type: String},
	created_date: {
		type: Date,
		default: Date.now
	}
});

export const NodeSchema = new Schema({
	nodename: {type: String},
	ipaddress: {type: String},
	community: {type: String},
	created_date: {
		type: Date,
		default: Date.now
	}
});

export const DataSchema = new Schema({
	nodename: {type: String},
	ipaddress: {type: String},
	community: {type: String},
	status: {
		type: String,
		default: 'Unknown'
	},
	created_date: {
		type: Date,
		default: Date.now
	}
});