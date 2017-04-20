from workers import aggregate_data, update_classifiers
import database_connection

if __name__ == "__main__":
    update_classifiers.run()
    aggregate_data.run()


