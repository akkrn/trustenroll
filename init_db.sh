#!/bin/bash

CONTAINER_NAME="postgres"  
DB_NAME="trustenroll"
DB_USER="postgres"

echo "Проверяю наличие базы данных $DB_NAME..."
docker exec -i $CONTAINER_NAME psql -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" | grep -q 1

echo "🚧 Применяю миграции Aerich..."
docker exec -i backend uv run aerich upgrade

echo "🚧 Вставляю тестовые данные..."
docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME <<EOF
INSERT INTO maincategory (id, name) VALUES
(1, 'CREDIT'),
(2, 'DEBIT'),
(3, 'NFC');

INSERT INTO subcategory (id, name, main_category_id) VALUES
(1, 'FDECS', 1),
(2, 'CARDVALET', 1),
(3, 'MYCARDINFO', 1),
(4, 'DIGITALCARDSERVICE', 1),
(5, 'DXONLINE', 1),
(6, 'DIGITALCARDSERVICE', 2),
(7, 'CARDNAV', 2),
(8, 'CARDVALET', 2),
(9, 'APPLEPAY', 3),
(10, 'GPAY', 3);
EOF
    echo "✅ Готово!"
